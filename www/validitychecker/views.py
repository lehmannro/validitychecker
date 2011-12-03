from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from validitychecker.models import Query

def results(request):
    if 'q' in request.GET:
        term = request.GET['q']

        print(term)

        return render_to_response('results.html', {'term': term},
                                  context_instance=RequestContext(request))
    else:
        return # 300 /index

def index(request):
    return render_to_response('home.html',context_instance=RequestContext(request, dict(target=reverse(results))))
