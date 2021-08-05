from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, message
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.utils.html import strip_tags
from datetime import datetime

from movies_app.settings import EMAIL_HOST_USER

from .models import Movies, ManagerRequest, User, Emails
from .decorators import admin_required, viewer_required, manager_required
from .forms import ViewerSignUpForm, ManagerSignUpForm

import pytz

class SignUpView(generic.TemplateView):
    template_name = 'registration/signup.html'

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_choose')
        else:
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
        raise Http404('')
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

    # https://api.trakt.tv
    # https://developer.imdb.com/?ref=ft_ds 
    pass

@login_required
@admin_required
def choose(request):
    return render(request, 'movies/choose.html')

@method_decorator([admin_required], name='dispatch')
class RegistrationsView(generic.ListView):
    template_name = 'movies/manager_requests.html'
    context_object_name = 'manager_requests'

    def get_queryset(self):
        """ Return all the requests. """
        return ManagerRequest.objects.all()

def about(request):
    return render(request, 'movies/documentation.html')

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
    template_name = 'registration/signup_form_manager.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

def send_email(data):
    data = {
        'subject': data.get('sub'),
        'message': data.get('mes'),
        'html_msg': data.get('html'),
        'email_address': data.get('email')
    }

    subject = data["subject"]
    msg = data["message"]
    recipient = data["email_address"]
    print(recipient)
    html_msg = data["html_msg"]
    if subject and msg and recipient:
        try:
            send_mail(subject, msg, EMAIL_HOST_USER, [recipient], fail_silently = False, html_message=html_msg)
        except message.BadHeaderError:
            response = HttpResponse('Invalid header found.')
        response = "Email sent."
    else:
        response = "Make sure all fields are entered and valid."

    tz = pytz.timezone('Europe/Athens')
    date_sent = datetime.now(tz=tz)

    email = Emails(sender=EMAIL_HOST_USER, subject=subject, body_message=message, recipient=recipient, date_sent=date_sent)
    email.save()

    return HttpResponse(response)


def make_request(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    reason = request.POST.get("reason")

    if ManagerRequest.objects.filter(username=username):
        return render(request, 'registration/signup_form_manager.html', {'message': 'Request with your username already exists'})

    mr = ManagerRequest(first_name=first_name, last_name=last_name, username=username, email=email, password=password, reason=reason)
    mr.save()

    admins = User.objects.filter(is_superuser=True)
    emails = [a.email for a in admins]

    html_content = render_to_string('movies/mail_admins.html')
    text_content = strip_tags(html_content)

    data = {
        'sub':'New Manager Registration Request',
        'mes': text_content,
        'html': html_content,
        'email': emails
    }
    send_email(data)

    return render(request, 'movies/request_made.html')

@login_required
@admin_required
def approved(request, username):
    user_obj = ManagerRequest.objects.get(username=username)
    user = User()
    user.first_name = user_obj.first_name
    user.last_name = user_obj.last_name
    user.username = user_obj.username
    user.email = user_obj.email
    user.password = make_password(user_obj.password)
    user.is_manager = user_obj.is_manager

    ManagerRequest.objects.get(username=username).delete()
    del user_obj

    html_content = render_to_string('movies/mail_manager.html')
    text_content = strip_tags(html_content)

    data = {
        'sub':'Your registration request is approved!',
        'mes': text_content,
        'html': html_content,
        'email': user.email
    }
    send_email(data)

    user.save()
    return render(request, 'movies/approved.html')