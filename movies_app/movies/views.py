from json.decoder import JSONDecodeError
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic

from .models import Movies, User
from .decorators import admin_required, viewer_required, manager_required
from .forms import ViewerSignUpForm, ManagerSignUpForm

import requests

class SignUpView(generic.TemplateView):
    template_name = 'registration/signup.html'

class ViewerSignUpView(generic.CreateView):

    model = User
    form_class = ViewerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'viewer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class ManagerSignUpView(generic.CreateView):

    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'movies/home.html')

@login_required
def index(request):
    data = Movies.objects.all()
    context = {'movies': data}
    return render(request, 'movies/index.html', context)

@login_required
def detail(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})

@login_required
@viewer_required
def rate(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    
    try:
        selected_rating = request.POST['rating']
    except MultiValueDictKeyError:
        return render(request, '404.html')
    movie.rating = round((float(movie.rating) + float(selected_rating)) / 2, 1)
    movie.save()
    return HttpResponseRedirect(reverse('index'))

@login_required
@manager_required
def create(request):
    return render(request, 'movies/add.html')

@login_required
@manager_required
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

@login_required
@manager_required
def delete(request, movie_id):

    movie_instance = get_object_or_404(Movies, pk=movie_id)
    del movie_instance
    Movies.objects.get(id=movie_id).delete()
    return HttpResponseRedirect(reverse('index'))

@login_required
@manager_required
def suggested(request):

    suggested_movies = {}
    i=1
    while i <= 100:
        try:
            response = requests.get('https://api.trakt.tv/movies/' + str(i))
        except ConnectionError:
            break
        try:
            result = response.json()
        except JSONDecodeError:
            response.status_code = 200
            break
        if not result:
            continue
        print(result)
        suggested_movies[i-1] = result
        i+=1
    if response.status_code != 200:
        return render(request, '404.html')

    # https://developer.imdb.com/?ref=ft_ds 
    return render(request, 'movies/suggested.html', {'suggested_movies': suggested_movies})

@login_required
@admin_required
def choose(request):
    return render(request, 'movies/choose.html')

def about(request):
    return render(request, 'movies/documentation.html')

