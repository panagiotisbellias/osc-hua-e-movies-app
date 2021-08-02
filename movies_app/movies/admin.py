from django.contrib import admin

from .models import Movies

class MovieAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Movie title and rating', {'fields': ['title', 'rating']}),
        ('Date information', {'fields': ['release_date']}),
    ]

admin.site.register(Movies, MovieAdmin)