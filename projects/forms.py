from django import forms
from .models import Project, ProjectFile


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = [
            "title",
            "description",
            "deadline",
            "status",
            "visibility",
        ]

class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['file']
