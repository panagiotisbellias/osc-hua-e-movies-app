from django.contrib import admin

from .models import Movies, User

admin.site.register(Movies)
admin.site.register(User)