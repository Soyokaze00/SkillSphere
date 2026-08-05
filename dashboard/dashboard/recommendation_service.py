import re
from dataclasses import dataclass

from django.db.models import QuerySet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from projects.models import Project


@dataclass
class ProjectRecommendation:
    project: Project
    score: int
    reason: str


def recommend_projects_for_user(
    user,
    limit: int = 4,
) -> list[ProjectRecommendation]:
    """
    Return public, open projects ranked by textual similarity
    to the user's profile.
    """

    candidate_projects = list(_get_candidate_projects(user)[:50])

    if not candidate_projects:
        return []

    user_text = _build_user_text(user)

    if not user_text:
        return _fallback_recommendations(
            projects=candidate_projects,
            limit=limit,
        )

    project_texts = [_build_project_text(project) for project in candidate_projects]

    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=1500,
        )

        document_matrix = vectorizer.fit_transform([user_text, *project_texts])

        similarity_scores = cosine_similarity(
            document_matrix[0:1],
            document_matrix[1:],
        ).flatten()

    except ValueError:
        return _fallback_recommendations(
            projects=candidate_projects,
            limit=limit,
        )

    ranked_projects = sorted(
        zip(candidate_projects, similarity_scores),
        key=lambda item: item[1],
        reverse=True,
    )

    recommendations = []

    for project, raw_score in ranked_projects[:limit]:
        score = max(
            1,
            min(99, round(float(raw_score) * 100)),
        )

        recommendations.append(
            ProjectRecommendation(
                project=project,
                score=score,
                reason=_build_reason(
                    user_text=user_text,
                    project=project,
                ),
            )
        )

    return recommendations


def _get_candidate_projects(user) -> QuerySet:
    return (
        Project.objects.filter(
            visibility=Project.PUBLIC,
            status="OPEN",
        )
        .exclude(owner=user)
        .exclude(memberships__user=user)
        .select_related("owner")
        .distinct()
        .order_by("-created_at")
    )


def _build_user_text(user) -> str:
    return _normalize_text(
        " ".join(
            [
                user.username or "",
                user.bio or "",
            ]
        )
    )


def _build_project_text(project: Project) -> str:
    return _normalize_text(
        " ".join(
            [
                project.title or "",
                project.description or "",
                project.tags or "",
            ]
        )
    )


def _normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[,;/|_-]+", " ", value)
    value = re.sub(r"[^\w\s]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _build_reason(
    user_text: str,
    project: Project,
) -> str:
    user_terms = {word for word in user_text.split() if len(word) >= 3}

    project_terms = {word for word in _build_project_text(project).split() if len(word) >= 3}

    matches = sorted(user_terms.intersection(project_terms))[:3]

    if matches:
        return "Matches your profile: " + ", ".join(matches)

    if project.tags:
        return "Suggested from project topics: " + ", ".join(project.tag_list[:3])

    return "Suggested based on your profile and project content"


def _fallback_recommendations(
    projects: list[Project],
    limit: int,
) -> list[ProjectRecommendation]:
    return [
        ProjectRecommendation(
            project=project,
            score=0,
            reason="Complete your bio for more personalized suggestions",
        )
        for project in projects[:limit]
    ]
