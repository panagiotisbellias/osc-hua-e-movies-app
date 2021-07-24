from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Movies

def index(request):
    data = Movies.objects.all()
    context = {'movies': data}
    return render(request, 'movies/index.html', context)

def detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})

def rate(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    
    try:
        selected_rating = request.POST['rating']
    except MultiValueDictKeyError:
        raise Http404('')
    movie.rating = round((float(movie.rating) + float(selected_rating)) / 2, 1)
    movie.save()
    return HttpResponseRedirect(reverse('index'))