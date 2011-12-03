from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ranking = models.IntegerField()

class Article(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    release_date = models.DateField()

