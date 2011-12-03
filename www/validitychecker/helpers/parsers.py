# -*- coding: utf-8 -*-
from lxml.html.soupparser import fromstring
import urllib, urllib2
from datetime import date

def google_scholar_parser (query):
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=0))
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    search_path = "http://scholar.google.com/scholar?hl=en&num=25&q=" + urllib.quote_plus(query) + "&as_sdt=0%2C5&as_ylo=&as_vis=1"
    print search_path
    response = opener.open(search_path)
    results = []
    doc = fromstring(response.read())
    for elem in doc.find_class('gs_r'):
        if elem.find_class('gs_rt')[0].find("h3/a/b") != None:
            elem.find_class('gs_rt')[0].find("h3/a/b").drop_tag()
        print elem.find_class('gs_a')[0].text
        if elem.find_class('gs_a')[0].find("b") != None:
            elem.find_class('gs_a')[0].find("b").drop_tag()
        print elem.find_class('gs_a')[0].text
        res = {}
        res['title'] = (elem.find_class('gs_rt')[0].find("h3/a").text)
        res['authors'] = (elem.find_class('gs_a')[0].text.split(' - ')[0].rstrip(u'\u2026 ')).split(',')
        res['publish_date'] = date(int(elem.find_class('gs_a')[0].text.split(' - ')[1].split(',')[-1]),1,1)
        res['url'] = urllib.quote_plus(elem.find_class('gs_rt')[0].find("h3/a").attrib['href'])
        results.append(res)
    return results

#print google_scholar_parser('CO2 has no influence on the climate')
