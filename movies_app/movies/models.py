from django.contrib.auth.models import AbstractUser
from django.db import models

class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    director = models.CharField(max_length=64)
    actors = models.TextField(max_length=512)
    genre = models.CharField(max_length=64)
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        verbose_name_plural = 'movies'

    def __str__(self):
        return f"ID: {self.id} - Title: {self.title} - Director: {self.director} - Actors: {self.actors} - Genre: {self.genre} - Release Date: {self.release_date} - Rating: {self.rating}"

class User(AbstractUser):
    is_viewer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)