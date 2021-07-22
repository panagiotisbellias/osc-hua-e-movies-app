from django.db import models

class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=60)
    actors = models.TextField(max_length=512)
    genre = models.CharField(max_length=40)
    release_date = models.DateField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        verbose_name_plural = 'movies'