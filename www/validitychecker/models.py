from django.db import models

class Author(models.Model):
    articles = models.ManyToManyField('Article', verbose_name="list of articles")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ranking = models.IntegerField()

class Article(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    publish_date = models.DateField('date published')

