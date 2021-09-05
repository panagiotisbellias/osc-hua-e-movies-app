from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.test import TestCase

from .models import ManagerRequest, User

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

    def newManagerRequest(self):
        username='manager_test'
        ManagerRequest.objects.create(
            first_name='Manager',
            last_name='Test',
            username = username,
            email = 'test@mail.com',
            password = 'managerpasswd',
            reason = 'test_reason',
            is_manager = True
        )
        return username

    # Viewer Registration
    def test_register_viewer(self):
        username = self.newViewer()
        print(f"Test 1.1.1: New Viewer with username '{username}' created")
        self.assertEquals(User.objects.get(is_viewer=True).username, 'viewer_test')
        print(f"Test 1.1.2: Viewer with username '{username}' is registered successfully")

    # Login Testing
    def test_loginning_in(self):
        self.newViewer()
        user = authenticate(username='viewer_test', password='viewerpasswd')
        print(f"Login Test: Check")
        self.assertIsNotNone(user)
        
    # Manager Registration
    def test_register_manager(self):
       User.objects.create(
           username='manager_test',
           password=make_password('managerpasswd'),
           is_manager=True
       )
       self.assertEquals(User.objects.get(is_manager=True).username, 'manager_test')

# Managers Use Case Tests
class ManagerTests(TestCase):

    # login as manager
    def test_loginning_in(self):
        pass

    # add movies
    def test_creating_movies(self):
        pass

    # delete movies
    def test_deleting_movies(self):
        pass

    # test api suggestion connections
    def test_api_connections(self):
        pass

    # add from there movies
    def test_creating_movies_from_api(self):
        pass

    pass

# Viewers Use Case Tests
class ViewerTests(TestCase):

    # login as viewer
    def test_loginning_in(self):
        pass

    # View Movies in a print
    def test_viewing_movies(self):
        pass

    # rate movies and view them again
    def test_rate_view_movies(self):
        pass

    pass

