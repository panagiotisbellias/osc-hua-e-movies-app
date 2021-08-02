from django.contrib.auth.hashers import make_password
from django.test import TestCase

from .models import User

class AuthenticationTests(TestCase):

    def test_register_viewer(self):
       User.objects.create(
           username='viewer_test',
           password=make_password('viewerpasswd'),
           is_viewer=True
       )
       self.assertEquals(User.objects.get(is_viewer=True).username, 'viewer_test')

    def test_register_manager(self):
       User.objects.create(
           username='manager_test',
           password=make_password('managerpasswd'),
           is_manager=True
       )
       self.assertEquals(User.objects.get(is_manager=True).username, 'manager_test')