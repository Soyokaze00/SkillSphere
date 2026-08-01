from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from users.models import CustomUser


@registry.register_document
class UserDocument(Document):

    username = fields.TextField(
        analyzer="autocomplete",
        search_analyzer="standard"
    )


    class Index:
        name = "users"

        settings = {
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 20,
                    }
                },
                "analyzer": {
                    "autocomplete": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                    }
                }
            }
        }


    class Django:
        model = CustomUser

        fields = [
            "id",
            "first_name",
            "last_name",
        ]