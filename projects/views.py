from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from projects.tasks import process_uploaded_file
from .models import Project, ProjectMember, ProjectFile
from .forms import ProjectForm, ProjectFileForm

@login_required
def create_project(request):
    project_form = ProjectForm(request.POST or None)
    file_form = ProjectFileForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = request.user
            project.save()
            
            if request.FILES.get('file'):
                if file_form.is_valid():
                    new_file = file_form.save(commit=False)
                    new_file.project = project
                    new_file.uploaded_by = request.user
                    new_file.save()
                    process_uploaded_file.delay(new_file.id)
            
            return redirect("projects:project-list")

    return render(
        request,
        "projects/create_project.html",
        {
            "project_form": project_form,
            "file_form": file_form
        }
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
    project = get_object_or_404(Project, id=project_id)

    if project.visibility == Project.PRIVATE:
        is_owner = project.owner == request.user
        is_member = ProjectMember.objects.filter(
            project=project, 
            user=request.user
        ).exists()

        if not (is_owner or is_member):
            return HttpResponseForbidden("You don't have access to this project.")
        
    file_form = ProjectFileForm()
    
    if request.method == "POST" and "file_upload" in request.POST:
        file_form = ProjectFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            new_file = file_form.save(commit=False)
            new_file.project = project
            new_file.uploaded_by = request.user
            new_file.save()
            
            process_uploaded_file.delay(new_file.id) 
            return redirect('projects:project-detail', project_id=project.id)

    return render(request, "projects/project_detail.html", {
        "project": project,
        "file_form": file_form
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
        'yml', 'ini', 'log', 'gitignore', 'env', 'Dockerfile', 
        'dockerignore','csv', 'tsv', 'docx', 'doc', 'rtf', 'odt',
        'pptx', 'ppt', 'xlsx', 'xls', 
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
    }
    return render(request, 'projects/file_detail.html', context)
