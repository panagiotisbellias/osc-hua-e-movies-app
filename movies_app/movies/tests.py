from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.test import TestCase

from datetime import datetime
from .models import User, Movies
import pytz

def createManager():
    user = User.objects.create(
        username='manager_test',
        password=make_password('managerpasswd'),
        is_manager=True
    )
    return user

def createMovie():
    tz = pytz.timezone('Europe/Athens')
    movie = Movies.objects.create(
        title='Test Movie',
        director='Test Director',
        actors='Test Actor 1, Test Actor 2',
        genre='Test Genre',
        release_date=datetime.now(tz=tz),
        rating='5.0'
    )
    return movie

# Auth Tests
class AuthenticationTests(TestCase):

    def newViewer(self):
        username='viewer_test'
        User.objects.create(
           username=username,
           password=make_password('viewerpasswd'),
           is_viewer=True
        )
        return username

    # Viewer Registration
    def test_register_viewer(self):
        username = self.newViewer()
        print(f"Test 1.3.1: New Viewer with username '{username}' created")
        self.assertEquals(User.objects.get(is_viewer=True).username, 'viewer_test')
        print(f"Test 1.3.2: Viewer with username '{username}' is registered successfully")

    # Login Testing
    def test_loginning_in(self):
        self.newViewer()
        user = authenticate(username='viewer_test', password='viewerpasswd')
        print(f"Test 1.1: Login Viewer Check")
        self.assertIsNotNone(user)
        
    # Manager Registration
    def test_register_manager(self):
       createManager()
       print(f"Test 1.2: Manager with username manager_test created and is registered successfully")
       self.assertEquals(User.objects.get(is_manager=True).username, 'manager_test')

# Managers Use Case Tests
class ManagerTests(TestCase):

    # login as manager
    def test_loginning_in(self):
        createManager()
        user = authenticate(username='manager_test', password='managerpasswd')
        print(f"Test 2.2: Login Manager Check")
        self.assertIsNotNone(user)

    # add movies
    def test_creating_movies(self):

        movie = createMovie()
        print(f"Test 2.1: Movie '{movie.title}' is created successfully on '{movie.release_date}'")
        self.assertIsNotNone(movie)

    # delete movies
    def test_deleting_movies(self):
        createMovie()
        movie_instance = Movies.objects.get(title='Test Movie')
        del movie_instance
        Movies.objects.get(title='Test Movie').delete()
        #self.assertIsNone(movie_instance)
        return True

    # test api suggestion connections
    def test_api_connections(self):
        pass

    # add from there movies
    def test_creating_movies_from_api(self):
        pass

    pass

# Viewers Use Case Tests
class ViewerTests(TestCase):

    # View Movies in a print
    def test_viewing_movies(self):
        pass

    # rate movies and view them again
    def test_rate_view_movies(self):
        pass

    pass

