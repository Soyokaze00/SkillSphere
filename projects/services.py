from users.models import Follow
from django.db.models import Q

def _can_access(project, user):
    """Same access rule as projects._user_can_access, duplicated here to
    avoid importing a "private" (underscore-prefixed) helper across apps."""
    from projects.models import Project, ProjectMember

    if project.visibility != Project.PRIVATE:
        return True
    if project.owner_id == user.id:
        return True
    return ProjectMember.objects.filter(project=project, user=user).exists()


def get_following_activity(user, limit=10):
    """
    Recent "X liked Y" / "X created Y" events from people `user` follows,
    merged into one timeline and access-filtered so a private project
    someone follows can't leak into a feed that shouldn't see it.
    """
    from projects.models import Project, ProjectLike

    following_ids = list(Follow.objects.filter(follower=user).values_list("following_id", flat=True))
    if not following_ids:
        return []

    items = []

    recent_likes = (
        ProjectLike.objects
        .filter(user_id__in=following_ids)
        .select_related("project", "user")
        .order_by("-created_at")[: limit * 2]
    )
    for like in recent_likes:
        if _can_access(like.project, user):
            items.append({
                "type": "liked",
                "actor": like.user,
                "project": like.project,
                "timestamp": like.created_at,
            })

    recent_created = (
        Project.objects
        .filter(owner_id__in=following_ids)
        .select_related("owner")
        .order_by("-created_at")[: limit * 2]
    )
    for project in recent_created:
        if _can_access(project, user):
            items.append({
                "type": "created",
                "actor": project.owner,
                "project": project,
                "timestamp": project.created_at,
            })

    items.sort(key=lambda item: item["timestamp"], reverse=True)
    return items[:limit]


def get_similar_projects(project, limit=4):
    """
    Similarity ranked by: number of shared tags, falling back to shared
    words in the title if a project has no tags. Only PUBLIC projects
    are considered -- 'similar' projects shown in a sidebar shouldn't
    leak private ones the viewer can't otherwise reach.
    """
    from django.db.models import Q
    from .models import Project

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


def get_trending_projects(limit=10, days=7):
    """
    Trending = most liked recently, weighted a bit by views so a brand
    new project with a couple likes can still surface. Falls back to
    all-time likes if nothing happened in the window (e.g. early on,
    when the whole site is quiet).
    """
    from django.db.models import Count, F
    from django.utils import timezone
    from datetime import timedelta
    from .models import Project

    since = timezone.now() - timedelta(days=days)

    recent = (
        Project.objects.filter(visibility=Project.PUBLIC)
        .annotate(recent_like_count=Count("likes", filter=Q(likes__created_at__gte=since)))
        .filter(recent_like_count__gt=0)
        .order_by("-recent_like_count", "-views_count")[:limit]
    )
    if recent.exists():
        return list(recent)

    return list(
        Project.objects.filter(visibility=Project.PUBLIC)
        .annotate(total_likes=Count("likes"))
        .order_by("-total_likes", "-views_count")[:limit]
    )