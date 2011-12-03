from django.db import models

class Author(models.Model):
    articles = models.ManyToManyField('Article', verbose_name="list of articles")
    name = models.CharField(max_length=60, verbose_name="name of the author")
    isi_score= models.IntegerField('ISI score', null=True)

    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField(blank=True)
    publish_date = models.DateField('date published')
    source = models.CharField(max_length=2048, blank=True)
    language = models.ForeignKey('Language', null=True)
    data_type = models.ForeignKey('Datatype', null=True)

    url = models.CharField(max_length=255)

    times_cited_on_isi = models.IntegerField(null=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.title

class Language(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=15)

class Datatype(models.Model):
    name = models.CharField(max_length=30)

class Query(models.Model):
    query = models.CharField(max_length=255)
    number = models.IntegerField()

    last_updated = models.DateTimeField(auto_now=True)
