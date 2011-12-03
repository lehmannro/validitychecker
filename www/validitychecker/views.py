from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from datetime import date
import urllib

from validitychecker.models import Query, Article, Author, Language, Datatype
from validitychecker.helpers import parsers

def results(request):
    if 'q' in request.GET:
        query = request.GET['q']

        #save query to db
        qobj, created = Query.objects.get_or_create(query=query, defaults={'query':query, 'number':0})
        qobj.number = F('number') + 1
        qobj.save()

        #query google scholar
        googleScholar = parsers.google_scholar_parser(query)

        #write to db
        englishLang, created = Language.objects.get_or_create(code='EN', defaults={'code':'EN', 'name':'English'})
        articleType, created = Datatype.objects.get_or_create(name='article', defaults={'name':'article'})
        for entry in googleScholar:
            article, created = Article.objects.get_or_create(title=entry[0], defaults={'title':entry[0], 'url':'www.rhok.org', 'publish_date':date.today(), 'language':englishLang, 'data_type':articleType})
            author, created = Author.objects.get_or_create(name=entry[1], defaults={'name':entry[1]})
            author.articles.add(article)

        titles = [x[0] for x in googleScholar]

        resultset = get_authors_and_articles_from_db(titles)
        #resultset = get_fake_results(query)

        return render_to_response('results.html',
                                  context_instance=RequestContext(request, dict(
                                  target=reverse(results), results=resultset, query=query)))
    else:
        return # 300 /index

def get_authors_and_articles_from_db(titles):
    """ 
    returns the matching articles and authors from the db 
    param: title a list of strings    
    """
    authors = Author.objects.filter(articles__title__in=titles)
    return [(author,Article.objects.filter(title__in=titles).filter(author__name=author.name)) for author in authors]

class MockAuthor(object):
    def __init__(self, name, score):
        self.first_name, self.last_name = name.rsplit(" ", 1)
        self.articles = self
        self.count = 100
        self.isi_score = score
class MockArticle(object):
    def __init__(self, title):
        self.title = title
        self.url = "http://google.com/"
        self.publish_date = date.today()

def get_fake_results(query):
    return [
            (MockAuthor("Al Gore", 100), [
                MockArticle("An Inconvenient Truth"),
                MockArticle("Our Choice")]),
            (MockAuthor("J R R Tolkien", 40), [
                MockArticle("Little Hobbit"),
                MockArticle("Lord of the Rings")])]

def index(request):

    popular_queries = Query.objects.order_by('-number')[:5]
    for q in popular_queries:
        q.url = urllib.quote_plus(q.query)

    return render_to_response('home.html',
                              { 'popular_queries': popular_queries },
                              context_instance=RequestContext(request, dict(
                              target=reverse(results))))

@csrf_exempt
def get_score(request):
    title = request.POST.get('title')
    author = request.POST.get('author')
    import random
    return HttpResponse(str(random.randrange(100)), mimetype="text/plain")
