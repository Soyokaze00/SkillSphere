from django.db.models import Q
from django.db.models import Count, Prefetch
from .models import Project, ProjectFile, ProjectMember
from projects.tasks import process_uploaded_file
import json

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB per file


def get_similar_projects(project, limit=4):
    """
    Similarity ranked by: number of shared tags, falling back to shared
    words in the title if a project has no tags. Only PUBLIC projects
    are considered -- 'similar' projects shown in a sidebar shouldn't
    leak private ones the viewer can't otherwise reach.
    """

    candidates = Project.objects.filter(
        visibility=Project.PUBLIC
    ).exclude(id=project.id).select_related("owner")

    project_tags = set(project.tag_list)

    if project_tags:
        tag_q = Q()
        for tag in project_tags:
            tag_q |= Q(tags__icontains=tag)
        candidates = candidates.filter(tag_q)

        scored = []
        for candidate in candidates:
            shared = project_tags & set(candidate.tag_list)
            if shared:
                scored.append((len(shared), candidate))

        scored.sort(key=lambda pair: (pair[0], pair[1].created_at), reverse=True)
        results = [c for _, c in scored[:limit]]
        if results:
            return results

    title_words = [w for w in project.title.split() if len(w) > 2]
    if title_words:
        word_q = Q()
        for word in title_words:
            word_q |= Q(title__icontains=word)
        title_matches = list(candidates.filter(word_q)[:limit])
        if title_matches:
            return title_matches

    return list(candidates.order_by("-created_at")[:limit])


def user_can_access(project, user):
    """Owner and members can always access; PUBLIC projects are open to any
    logged-in user."""
    if project.visibility != Project.PRIVATE:
        return True
    if project.owner == user:
        return True
    return ProjectMember.objects.filter(project=project, user=user).exists()


def split_relative_path(raw_name):
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


def save_uploaded_files(request, project):
    """
    Save every file the user selected and kick off background processing 
    for each. Returns a list of error strings for files that were rejected 
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
        relative_path, filename = split_relative_path(raw_name)
        f.name = filename or f.name

        new_file = ProjectFile.objects.create(
            project=project,
            file=f,
            uploaded_by=request.user,
            relative_path=relative_path,
        )
        process_uploaded_file.delay(new_file.id)

    return errors
