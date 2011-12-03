from django.db import models

class Author(models.Model):
    articles = models.ManyToManyField('Article', verbose_name="list of articles")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    isi_score= models.IntegerField('ISI score')

    def name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

class Article(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    publish_date = models.DateField('date published')
    language = models.ForeignKey('Language')
    data_type = models.ForeignKey('Datatype')
    times_cited_on_isi = models.IntegerField()

    def __unicode__(self):
        return u'%s' % self.title

class Language(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=30)

class Datatype(models.Model):
    name = models.CharField(max_length=30)
