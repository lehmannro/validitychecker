from django.shortcuts import render_to_response

def index(request):
    return render_to_response('home.html',
                              context_instance=RequestContext(request))
