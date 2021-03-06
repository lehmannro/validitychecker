from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'www.validitychecker.views.index', name='home'),
    url(r'^search/?$', 'www.validitychecker.views.results'),
    url(r'^score/?$', 'www.validitychecker.views.get_score'),
     url(r'^statistics/?$', 'www.validitychecker.views.statistics'),
    # url(r'^www/', include('www.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
