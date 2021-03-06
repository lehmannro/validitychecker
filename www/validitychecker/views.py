from django.core.urlresolvers import reverse
from django.db.models import F, Count, Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from random import shuffle, seed
import math

from datetime import date
import urllib

from validitychecker.models import Query, Article, Author, Language, Datatype
from validitychecker.helpers import parsers, IsiHandler, gviz_api

def results(request):
    if 'q' in request.GET:
        query = request.GET['q']

        #save query to db
        qobj, created = Query.objects.get_or_create(query=query, defaults={'query':query, 'number':0})
        qobj.number = F('number') + 1
        qobj.save()

        #query google scholar
        googleScholar = parsers.google_scholar_parser(query)

        newArticles = []

        #write to db
        articleType, created = Datatype.objects.get_or_create(name='article', defaults={'name':'article'})
        for entry in googleScholar:
            article, created = Article.objects.get_or_create(
                title=entry['title'],
                defaults={
                    'url':entry['url'], 
                    'publish_date':entry['publish_date'],
                    'title':entry['title'], 
                    'data_type':articleType,
                    'abstract':entry['abstract']
                })
            if created:
                #prepare new articles that have to be 
                newArticles.append(article)
            for authorName in entry['authors']:
                author, created = Author.objects.get_or_create(name=authorName, defaults={'name':authorName})
                author.articles.add(article)
                author.save()
                #print author.name
                #for x in author.articles.all():
                #    print x.title

        titles = [x['title'] for x in googleScholar]

        #calculate isi cites for new articles
        calculateIsiCites(newArticles)

        calcISIForUnratedAuthors()

        resultset = get_authors_and_articles_from_db(titles)
        
        for author, articles in resultset:
            author.url = urllib.quote_plus(author.name)
        #resultset = get_fake_results(query)

        return render_to_response('results.html',
                                  context_instance=RequestContext(request, dict(
                                  target=reverse(results), results=resultset, query=query)))
    else:
        return # 300 /index

def calculateIsiCites(newArticles):
    #fetch data for new articles
    for article in newArticles:
        IsiHandler.refreshArticles(article)

def calcISIForUnratedAuthors():
    for author in get_unrated_authors():
        author.isi_score = IsiHandler.calcISIScoreWithArticles(author.name,author.articles.values_list('title', flat=True))
        author.save()

def get_unrated_authors():
    """
    Get all the authors that have no ISI-Score yet
    """
    return Author.objects.filter(isi_score=None)

def get_authors_and_articles_from_db(titles):
    """ 
    returns the matching articles and authors from the db that are credible
    param: title a list of strings    
    """
    ret = []
    authors = Author.objects.filter(isi_score__gt=0, articles__title__in=titles).annotate(isi_cites=Sum('articles__times_cited_on_isi')).distinct()[:8]
    for author in authors:
        tmp = (author, Article.objects.filter(title__in=titles, author__name=author.name).order_by('-publish_date'))
        #calculate score
        if not tmp[0].isi_cites:
            tmp[0].isi_cites = 0
        tmp[0].score = int(math.log(tmp[0].isi_cites+1) + 2*tmp[0].isi_score)
        ret.append(tmp)
    ret = sorted(ret, key=lambda elem: -elem[0].score)
    return ret

def get_unrated_authors():
    """
    Get all the authors that have no ISI-Score yet
    """
    return Author.objects.filter(isi_score=None)


def index(request):
    popular_queries = list(Query.objects.order_by('-number')[:15])
    seed(42)
    shuffle(popular_queries)
    for q in popular_queries:
        q.url = urllib.quote_plus(q.query)

    return render_to_response('home.html',
                              { 'popular_queries': popular_queries },
                              context_instance=RequestContext(request, dict(
                              target=reverse(results))))

def statistics(request):
    description = {"publications": ("number", "Publications"),
                 "cg_score": ("number", "Climate Goggles Score"),
                 "isi_score": ("number", "Isi Score")}
    data = [{'isi_score': author.isi_score, 'publications': author.publications} for author  in Author.objects.annotate(publications=Count('articles'))]
    scatter_data_table = gviz_api.DataTable(description)
    scatter_data_table.LoadData(data)
    json = scatter_data_table.ToJSCode("data",columns_order=("publications", "cg_score", "isi_score"))

    return render_to_response('statistics.html',
                              {'scatter': json },
                              context_instance=RequestContext(request, dict(target=reverse(results))))

@csrf_exempt
def get_score(request):
    title = request.POST.get('title')
    author = request.POST.get('author')
    import random
    return HttpResponse(str(random.randrange(100)), mimetype="text/plain")
