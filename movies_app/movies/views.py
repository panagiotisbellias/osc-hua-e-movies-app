from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Movies

def home(request):
    return render(request, 'movies/home.html')

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

def create(request):
    return render(request, 'movies/add.html')

def new_movie(request):
    movie = Movies(title = request.POST.get("title"), director = request.POST.get("director"), actors = request.POST.get('actors'),
    genre = request.POST.get('genre'), release_date = request.POST.get('release_date'), rating = 0.0
    )
    movie.save()
    movie = get_object_or_404(Movies, pk=movie.id)
    if movie:
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('create'))

def delete(request, movie_id):

    movie_instance = get_object_or_404(Movies, pk=movie_id)
    del movie_instance
    Movies.objects.get(id=movie_id).delete()
    return HttpResponseRedirect(reverse('index'))

def suggested(request):

    # https://api.trakt.tv
    # https://developer.imdb.com/?ref=ft_ds 
    pass