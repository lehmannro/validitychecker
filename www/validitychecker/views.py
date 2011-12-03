from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from validitychecker.models import Query, Article, Author
from datetime import date
from django.db.models import F

def results(request):
    if 'q' in request.GET:
        query = request.GET['q']

        #save query to db
        qobj, created = Query.objects.get_or_create(query=query, defaults={'query':query, 'number':0})
        qobj.number = F('number') + 1
        qobj.save()

        #query google scholar
        #how?

        resultset = get_fake_results(query)
        return render_to_response('results.html',
                                  context_instance=RequestContext(request, dict(
                                  results=resultset, query=query)))
    else:
        return # 300 /index

def get_authors_and_articles_from_db(titles):
    """ 
    returns the matching articles and authors from the db 
    param: title a list of strings    
    """
    return Author.objects.filter(articles__title__in=title)

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
    return render_to_response('home.html',
                              { 'popular_queries': popular_queries },
                              context_instance=RequestContext(request, dict(
                              target=reverse(results))))
