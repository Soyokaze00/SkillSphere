from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Project


@registry.register_document
class ProjectDocument(Document):

    title = fields.TextField(
        analyzer="autocomplete",
        search_analyzer="standard",
    )

    description = fields.TextField(
        analyzer="autocomplete",
        search_analyzer="standard",
    )

    tags = fields.TextField(
        analyzer="autocomplete",
        search_analyzer="standard",
    )

    class Index:
        name = "projects"

        settings = {
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 20,
                    }
                },
                "analyzer": {
                    "autocomplete": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter",
                        ],
                    }
                },
            }
        }

    class Django:
        model = Project

        fields = [
            "id",
            "status",
            "visibility",
            "created_at",
        ]