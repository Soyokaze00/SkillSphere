from django.db.models import Q
from django.db.models import Count, Prefetch
from .models import Project, ProjectFile



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

