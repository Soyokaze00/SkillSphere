from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .models import Project, ProjectMember
from .forms import ProjectForm
from django.db.models import Q

# Create your views here.

@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("projects:project-list")

    return render(
        request,
        "projects/create_project.html",
        {"form": form}
    )



@login_required
def project_list(request):

    projects = Project.objects.filter(
        Q(owner=request.user)
        |
        Q(memberships__user=request.user)
    ).distinct()

    return render(
        request,
        "projects/project_list.html",
        {"projects": projects}
    )


@login_required
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if project.visibility == Project.PRIVATE:

        is_owner = project.owner == request.user

        is_member = ProjectMember.objects.filter(
            project=project,
            user=request.user
        ).exists()

        if not (is_owner or is_member):
            return HttpResponseForbidden(
                "You don't have access to this project."
            )

    return render(
        request,
        "projects/project_detail.html",
        {"project": project}
    )