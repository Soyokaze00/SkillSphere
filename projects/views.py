import io
import os
import json
import zipfile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from notifications.utils import create_notification
from projects.tasks import process_uploaded_file
from django.utils import timezone
from .models import Project, ProjectMember, ProjectFile, ProjectLike, Comment, ProjectInvitation
from .forms import ProjectForm, ProjectFileForm, InviteMemberForm
from django.urls import reverse
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from users.models import Follow
from .services import get_similar_projects
from django.core.paginator import Paginator


MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB per file


def _user_can_access(project, user):
    """Owner and members can always access; PUBLIC projects are open to any
    logged-in user."""
    if project.visibility != Project.PRIVATE:
        return True
    if project.owner == user:
        return True
    return ProjectMember.objects.filter(project=project, user=user).exists()


def _split_relative_path(raw_name):
    """
    Folder uploads arrive with a name like 'my-project/src/main.py'
    (see the folderInput JS, which renames each File to its
    webkitRelativePath before appending it to the form). This pulls that
    apart into a safe relative path and a bare filename, stripping any
    '.', '..', or empty segments so nothing can escape the upload folder.
    """
    segments = [
        s for s in raw_name.replace("\\", "/").split("/")
        if s not in ("", ".", "..")
    ]
    if not segments:
        return "", raw_name

    filename = segments[-1]
    relative_path = "/".join(segments) if len(segments) > 1 else ""
    return relative_path, filename


def _save_uploaded_files(request, project):
    """
    Save every file the user selected and kick off background processing 
    for each. Returns a list of error stringsfor files that were rejected 
    (too large), so the view can show them.
    """
    errors = []
    files = request.FILES.getlist('file')

    try:
        raw_paths = json.loads(request.POST.get('file_paths', '[]'))
    except (ValueError, TypeError):
        raw_paths = []

    for i, f in enumerate(files):
        if f.size > MAX_FILE_SIZE:
            errors.append(f"{f.name} is too large (max {MAX_FILE_SIZE / (1024 * 1024)} MB).")
            continue

        raw_name = raw_paths[i] if i < len(raw_paths) and raw_paths[i] else f.name
        relative_path, filename = _split_relative_path(raw_name)
        f.name = filename or f.name

        new_file = ProjectFile.objects.create(
            project=project,
            file=f,
            uploaded_by=request.user,
            relative_path=relative_path,
        )
        process_uploaded_file.delay(new_file.id)

    return errors


@login_required
def create_project(request):
    project_form = ProjectForm(request.POST or None)
    file_form = ProjectFileForm(request.POST or None, request.FILES or None)


    if request.method == "POST":
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()
  
            create_notification(
               user=project.owner,
               title="New project created",
               message=f"The project '{project.title}' has been created.", 
               notification_type="project",
               link=f"/projects/{project.id}/",
             )
            
            file_errors = _save_uploaded_files(request, project)
            for err in file_errors:
                messages.warning(request, err)

            return redirect("projects:project-list")
        
    return render(
        request,
        "projects/create_project.html",
        {
            "project_form": project_form,
            "file_form": file_form,
        }
    )


@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(owner=request.user) | Q(memberships__user=request.user)
    ).distinct()

    query = request.GET.get('q', '').strip()
    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

    projects = projects.order_by('-created_at')

    paginator = Paginator(projects, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {"page_obj": page_obj, "query": query , "page_title":"My Projects"}

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "projects/project_results.html", context)

    return render(
        request,
        "projects/project_list.html", 
        context
    )


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    total_size = sum(f.file.size for f in project.files.all())
    project_count = Project.objects.filter(owner=request.user).count()

    if project.visibility == Project.PRIVATE:
        if not _user_can_access(project, request.user):
            return HttpResponseForbidden("You don't have access to this project.")

    if request.method == "POST" and "add_comment" in request.POST:
        text = request.POST.get("text", "").strip()
        if text:
            Comment.objects.create(project=project, user=request.user, text=text)
            if project.owner != request.user:
                    create_notification(
                           user=project.owner,
                           title="New comment",
                           message=f"{request.user.username} commented on your project {project.title}",
                           notification_type="comment",
                           link=f"/projects/{project.id}/",
                 )
        return redirect('projects:project-detail', project_id=project.id)

    if request.method == "POST" and "invite_member" in request.POST:
        if project.owner != request.user:
            return HttpResponseForbidden("Only the project owner can invite collaborators.")

        invite_form = InviteMemberForm(request.POST)
        if invite_form.is_valid():
            email = invite_form.email
            matched_user = invite_form.matched_user

            if matched_user == project.owner:
                messages.warning(request, "That's already you -- you're the owner.")
            elif matched_user and ProjectMember.objects.filter(
                project=project, user=matched_user
            ).exists():
                messages.info(request, f"{matched_user.username} is already a collaborator.")
            elif ProjectInvitation.objects.filter(
                project=project, email__iexact=email, status=ProjectInvitation.PENDING
            ).exists():
                messages.info(request, f"An invite is already pending for {email}.")
            else:
                invitation = ProjectInvitation.objects.create(
                    project=project,
                    email=email,
                    invited_by=request.user,
                )

                accept_url = request.build_absolute_uri(
                    reverse("projects:invite-landing", args=[invitation.token])
                )
                greeting = f"Hi {matched_user.username}," if matched_user else "Hi there,"

                try:
                    send_mail(
                        subject=f"{request.user.username} invited you to collaborate on {project.title}",
                        message=(
                            f"{greeting}\n\n"
                            f"{request.user.username} invited you to collaborate on the "
                            f"SkillSphere project \"{project.title}\".\n\n"
                            f"Accept the invite here:\n{accept_url}\n\n"
                            f"If you weren't expecting this, you can ignore this email."
                        ),
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                    messages.success(request, f"Invite sent to {email}.")
                except Exception:
                    invitation.delete()
                    messages.error(
                        request, "Could not send the invite email right now. Please try again later."
                    )
        else:
            for error in invite_form.errors.get("identifier", []):
                messages.error(request, error)

        return redirect('projects:project-detail', project_id=project.id)

    viewed = request.session.setdefault('viewed_projects', [])
    if project.id not in viewed:
        project.views_count += 1
        project.save(update_fields=['views_count'])
        viewed.append(project.id)
        request.session.modified = True

    is_following_owner = (
        request.user != project.owner
        and Follow.objects.filter(follower=request.user, following=project.owner).exists()
    )

    return render(request, "projects/project_detail.html", {
        "project": project,
        "invite_form": InviteMemberForm(),
        "total_size": total_size,
        "views_count": project.views_count,
        "project_count": project_count,
        "is_liked": project.is_liked_by(request.user),
        "comments": project.comments.select_related("user").all(),
        "members": project.memberships.select_related("user").all(),
        "pending_invitations": project.invitations.filter(status=ProjectInvitation.PENDING),
        "is_following_owner": is_following_owner,
        "owner_follower_count": project.owner.followers.count(),
        "related_projects": get_similar_projects(project, limit=4),
        "file_tree_json": json.dumps(_serialize_tree(_build_file_tree(project.files.all()))),
        "page_title": project.title,
    })


def file_detail(request, file_id):
    project_file = get_object_or_404(ProjectFile, id=file_id)
    
    file_extension = project_file.file.name.split('.')[-1].lower()
    
    image_exts = [
        'jpg', 'jpeg', 'png', 'gif', 'svg', 'webp', 'bmp', 'ico', 
        'tiff', 'heic', 'heif' 
    ]

    code_and_text_exts = [
        'py', 'js', 'html', 'css', 'json', 'txt', 'md', 'c', 'cpp', 
        'java', 'rb', 'php', 'ts', 'sh', 'bash', 'sql', 'xml', 'yaml', 
        'yml', 'ini', 'log', 'gitignore', 'env', 'Dockerfile', 'go', 'kt', 
        'dockerignore', 'csv', 'tsv', 'jl', 'r', 'pl', 'swift', 'scala',
        'rs', 'dart', 'lua', 'hs', 'erl', 'ex', 'exs', 'clj', 'cljs', 
        'groovy', 'vbs', 'ps1', 'bat', 'cmd',
    ]


    file_content = None
    is_text = False
    
    if file_extension in code_and_text_exts:
        is_text = True
        try:
            with project_file.file.open('rb') as f:
                raw_data = f.read()
                
                try:
                    file_content = raw_data.decode('utf-8')
                except UnicodeDecodeError:
                    file_content = raw_data.decode('latin-1')
                    
        except Exception as e:
            file_content = f"Error loading preview: {str(e)}"

    context = {
        'project_file': project_file,
        'extension': file_extension,
        'is_image': file_extension in image_exts,
        'is_pdf': file_extension == 'pdf',
        'is_previewable_text': is_text,
        'file_content': file_content,
        "page_title": f"File: {project_file.filename}",
        
    }
    return render(request, 'projects/file_detail.html', context)


@login_required
@require_POST
def toggle_like(request, project_id):
    """
    Toggle the current user's like on a project. Returns JSON so the
    template can update the heart icon + count without a full page reload.
    """
    project = get_object_or_404(Project, id=project_id)

    if not _user_can_access(project, request.user):
        return HttpResponseForbidden("You don't have access to this project.")

    like, created = ProjectLike.objects.get_or_create(
        project=project,
        user=request.user,
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        
    if liked and project.owner != request.user: 
        create_notification(
                       user=project.owner,
                       title="New Like",
                       message=f"{request.user.username} liked your project '{project.title}'.",  # 👈 بگو کی لایک کرد
                       notification_type="like",
                       link=f"/projects/{project.id}/",
        )
        
    return JsonResponse({
        "liked": liked,
        "like_count": project.like_count,
    })


@login_required
@require_POST
def remove_member(request, project_id, user_id):
    """
    Owner-only: remove a collaborator from the project. Removing a member
    revokes their access to PRIVATE projects immediately.
    """
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Only the project owner can remove collaborators.")

    membership = ProjectMember.objects.filter(project=project, user_id=user_id).first()
    if membership:
        removed_username = membership.user.username
        membership.delete()
        messages.success(request, f"{removed_username} was removed from this project.")
    else:
        messages.info(request, "That user isn't a collaborator on this project.")

    return redirect('projects:project-detail', project_id=project.id)


@login_required
def invite_landing(request, token):
    invitation = get_object_or_404(ProjectInvitation, token=token)
    project = invitation.project

    if invitation.status != ProjectInvitation.PENDING:
        messages.info(request, "This invite has already been used or is no longer valid.")
        return redirect('projects:project-detail', project_id=project.id)

    email_mismatch = (
        not request.user.email
        or request.user.email.lower() != invitation.email.lower()
    )

    if request.method == "POST":
        if email_mismatch:
            messages.error(
                request,
                f"This invite was sent to {invitation.email}. Log in with that account to respond."
            )
            return redirect('projects:project-list')

        if "accept" in request.POST:
            ProjectMember.objects.get_or_create(project=project, user=request.user)
            invitation.mark_accepted()
            create_notification(
                user=project.owner,
                title="Invite accepted",
                message=f"{request.user.username} accepted your invite to '{project.title}'.",
                notification_type="invite",
                link=f"/projects/{project.id}/",
            )
            messages.success(request, f"You've joined \"{project.title}\" as a collaborator.")
            return redirect('projects:project-detail', project_id=project.id)

        elif "decline" in request.POST:
            invitation.mark_declined()
            create_notification(
                user=project.owner,
                title="Invite declined",
                message=f"{invitation.email} declined your invite to '{project.title}'.",
                notification_type="invite",
                link=f"/projects/{project.id}/",

            )
            messages.info(request, f"You declined the invite to \"{project.title}\".")
            return redirect('projects:project-list')

    return render(request, "projects/invite_landing.html", {
        "invitation": invitation,
        "project": project,
        "email_mismatch": email_mismatch,
    })


@login_required
@require_POST
def cancel_invite(request, project_id, invitation_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Only the project owner can cancel invites.")

    invitation = get_object_or_404(
        ProjectInvitation, id=invitation_id, project=project, status=ProjectInvitation.PENDING
    )
    invitation.status = ProjectInvitation.CANCELLED
    invitation.responded_at = timezone.now()
    invitation.save(update_fields=["status", "responded_at"])

    messages.success(request, f"Invite to {invitation.email} cancelled.")
    return redirect('projects:project-detail', project_id=project.id)


@login_required
@require_POST
def share_project_email(request, project_id):
    """
    Sends the project link directly to a recipient's inbox using the
    app's own SMTP account (the same one EMAIL_HOST_USER/PASSWORD in
    settings already use for verification emails) -- no Gmail app or
    OS share sheet involved.
    """
    project = get_object_or_404(Project, id=project_id)

    if not _user_can_access(project, request.user):
        return HttpResponseForbidden("You don't have access to this project.")

    try:
        payload = json.loads(request.body)
    except (ValueError, TypeError):
        payload = {}

    recipient = (payload.get("recipient_email") or "").strip()

    try:
        validate_email(recipient)
    except ValidationError:
        return JsonResponse(
            {"error": "That doesn't look like a valid email address."},
            status=400,
        )

    project_url = request.build_absolute_uri(
        reverse("projects:project-detail", args=[project.id])
    )

    try:
        send_mail(
            subject=f"{request.user.username} shared a project with you: {project.title}",
            message=(
                f"{request.user.username} shared a SkillSphere project with you.\n\n"
                f"{project.title}\n"
                f"{project.description[:200]}\n\n"
                f"View it here: {project_url}"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception:
        return JsonResponse(
            {"error": "Could not send the email right now. Please try again later."},
            status=500,
        )

    return JsonResponse({"sent": True})

@login_required
def download_all_files(request, project_id):
    """
    Bundle every file attached to a project into a single zip and stream
    it back as a download.
    """
    project = get_object_or_404(Project, id=project_id)

    if not _user_can_access(project, request.user):
        return HttpResponseForbidden("You don't have access to this project.")

    files = list(project.files.all())
    if not files:
        messages.warning(request, "This project has no files to download.")
        return redirect('projects:project-detail', project_id=project.id)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        used_names = set()
        for project_file in files:
            try:
                with project_file.file.open("rb") as f:
                    data = f.read()
            except Exception:
                continue

            name = project_file.display_path
            base_name, counter = name, 1
            while name in used_names:
                stem, ext = os.path.splitext(base_name)
                name = f"{stem} ({counter}){ext}"
                counter += 1
            used_names.add(name)

            zip_file.writestr(name, data)

    buffer.seek(0)
    safe_title = "".join(
        c for c in project.title if c.isalnum() or c in (" ", "-", "_")
    ).strip() or "project"

    project.download_count += 1
    project.save(update_fields=['download_count'])

    response = HttpResponse(buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{safe_title}.zip"'
    return response


def _build_file_tree(files):
    """
    Nests files into folders based on relative_path, e.g.
    'dashboard/static/dashboard/js/main.js' becomes
    dashboard -> static -> dashboard -> js -> main.js
    """
    root = {"folders": {}, "files": []}

    for f in files:
        if not f.relative_path:
            root["files"].append(f)
            continue

        parts = f.relative_path.split("/")
        node = root
        for part in parts[:-1]:
            node = node["folders"].setdefault(part, {"folders": {}, "files": []})
        node["files"].append(f)

    return root


def _serialize_tree(node):
    return {
        "folders": {
            name: _serialize_tree(sub)
            for name, sub in sorted(node["folders"].items())
        },
        "files": [
            {
                "id": f.id,
                "name": f.filename,
                "size": f.file.size,
                "detail_url": reverse("projects:file-detail", args=[f.id]),
                "download_url": f.file.url,
            }
            for f in sorted(node["files"], key=lambda x: x.filename)
        ],
    }


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Only the project owner can edit this project.")

    file_form = ProjectFileForm()

    if request.method == "POST" and "file_upload" in request.POST:
        if request.FILES.getlist('file'):
            file_errors = _save_uploaded_files(request, project)
            for err in file_errors:
                messages.warning(request, err)
        else:
            messages.warning(request, "No files were selected for upload.")
        return redirect('projects:project-edit', project_id=project.id)

    if request.method == "POST":
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            messages.success(request, "Project updated.")
            return redirect('projects:project-detail', project_id=project.id)
    else:
        project_form = ProjectForm(instance=project)

    return render(request, "projects/edit_project.html", {
        "project_form": project_form,
        "file_form": file_form,
        "project": project,
        "tags_json": json.dumps(project.tag_list),
        "page_title": f"Edit {project.title}",
    })


@login_required
@require_POST
def delete_project(request, project_id):
    """
    Permanently deletes a project and everything attached to it. Owner
    must retype the exact project title as a confirmation -- checked
    server-side, since a client-side-only check can be bypassed by
    just POSTing directly.
    """
    project = get_object_or_404(Project, id=project_id)

    if project.owner != request.user:
        return HttpResponseForbidden("Only the project owner can delete this project.")

    confirm_title = request.POST.get("confirm_title", "").strip()
    if confirm_title != project.title:
        messages.error(request, "The project name you typed didn't match. Nothing was deleted.")
        return redirect('projects:project-edit', project_id=project.id)

    for project_file in project.files.all():
        project_file.file.delete(save=False)

    project_title = project.title
    project.delete()

    messages.success(request, f'"{project_title}" was permanently deleted.')
    return redirect('projects:project-list')


@login_required
def explore_projects(request):
    projects = (
        Project.objects
        .filter(visibility=Project.PUBLIC)
        .exclude(owner=request.user)
        .exclude(memberships__user=request.user)
        .select_related("owner")
        .order_by("-created_at")
    )

    paginator = Paginator(projects, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "projects/explore.html", {
        "page_obj": page_obj,
        "page_title": "Explore",
    })