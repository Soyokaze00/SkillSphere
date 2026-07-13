# search/views.py
from django.shortcuts import render

def search_view(request):
    query = request.GET.get('q', '')
    return render(request, 'search/search.html', {'query': query})