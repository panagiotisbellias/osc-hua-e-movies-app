from django.shortcuts import get_object_or_404, render
from .models import Movies

def index(request):
    data = Movies.objects.all()
    context = {'movies': data}
    return render(request, 'movies/index.html', context)

def detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})