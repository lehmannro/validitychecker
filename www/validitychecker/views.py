from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

def results(request):
    if 'q' in request.GET:
        query = request.GET['q']
        resultset = get_results(query)
        return render_to_response('results.html',
                                  context_instance=RequestContext(request, dict(
                                  results=resultset, query=query)))
    else:
        return # 300 /index

def get_results(query):
    return ["%s 1" % query, "%s 2" % query]

def index(request):
    return render_to_response('home.html',
                              context_instance=RequestContext(request, dict(
                              target=reverse(results))))
