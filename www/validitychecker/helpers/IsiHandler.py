import urllib
import urllib2

from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from lxml.html import *
import re

standardPostData = {'SinceLastVisit_DATE'		:'',
                    'SinceLastVisit_UTC'		:'',
                    'action'					:'search',
                    'collapse_alt'				:'Collapse these settings',
                    'collapse_title'			:'Collapse these settings',
                    'defaultCollapsedListStatus':'display: none',
                    'defaultEditionsStatus'     :'display: block',
                    'endYear'					:'2011',
                    'expand_alt'				:'Expand these settings',
                    'expand_title'				:'Expand these settings',
                    'input_invalid_notice'		:'Search Error: Please enter a search term.',
                    'input_invalid_notice_limits':'<br/>Note: Fields displayed in scrolling boxes must be combined with at least one other search field.',
                    'limitStatus'				:'collapsed',
                    'period'					:'Range Selection',
                    'product'					:'WOS',
                    'range'						:'ALL',
                    'rsStatus'					:'display:none',
                    'rs_rec_per_page'			:'50',
                    'rs_refinePanel'			:'visibility:show',
                    'rs_sort_by'				:'RS.D',
                    'search_mode'				:'GeneralSearch',
                    'ssStatus'					:'display: none',
                    'ss_lemmatization'			:'On',
                    'ss_query_language'			:'',	
                    'startYear'					:'1899',
                    'timeSpanCollapsedListStatus':'display: none',
                    'timespanStatus'			:'display: block',
                    'value(limitCount)'			:'14',
                    'value(select2)'			:'LA',
                    'value(select3)'			:'DT',
                    'x'							:'37',
                    'y'							:'10',
                    'value(input1)'				:'',
                    'value(input2)'				:'',
                    'value(input3)'				:'',
                    'value(select1)'			:'TI',
                    'value(select2)'			:'AU',
                    'value(select3)'			:'SO',
                    'value(bool_1_2)'			:'AND',
                    'value(bool_2_3)'			:'AND',
                    'value(hidInput1)'			:'',
                    'value(hidInput2)'			:'initAuthor',
                    'value(hidInput3)'			:'initSource'
}

regexSuite = {'highlite': re.compile('<span class="hitHilite">(.*?)</span>',re.DOTALL),
                'author': re.compile('Author\(s\): </span>\s*(.*?)<br',re.DOTALL),
                'source': re.compile('Source:.*?</span>\s*(.*?)<span', re.DOTALL),
                'title' : re.compile('<value lang_id=.*?>(.*?)</value>', re.DOTALL),
                'timescited': re.compile('>([0-9]*?)</a> \(from', re.DOTALL),
                'extrachars': re.compile('&#[0-9]*?;')}

class IsiHandler():

    """class holding all the data needed for a Query to the ISI-Database"""

    def __init__(self, author='', title=''):
        self.opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPCookieProcessor())
        self.title=title
        self.author=author
        self.url='http://apps.webofknowledge.com/WOS_GeneralSearch.do'
        self.firstConnect()
        self.page=self.getPage(self.createPostQuery())
        self.ISIData = self.parsePage()
        print self.ISIData

    def firstConnect(self):
        req = urllib2.Request(self.url)
        response = self.opener.open(req)
		
    def createPostQuery(self):
        postdata = standardPostData
        postdata['value(input1)'] = self.title
        postdata['value(input2)'] = self.author
        data = urllib.urlencode(postdata)
        for edition in ['SCI', 'SSCI', 'AHCI']:
            data += '&editions=%s' % edition
        return urllib2.Request(self.url,data)

    def getPage(self, req):
        response = self.opener.open(req)
        return fromstring(response.read())

    def replaceAllHighlites(self, text):
        while regexSuite['highlite'].search(text) != None:
            innertext = regexSuite['highlite'].search(text).group(1)
            text = regexSuite['highlite'].sub(innertext,text,1)
        return text

    def getNumberOfRecords(self):
        pagereverse = tostring(self.page)[::-1]
        match = re.search('([0-9]*?)_DROCER', pagereverse)			#search for last record
        if match != None:
            return int(match.group(1)[::-1])
        else:
            return -1		

    def parsePage(self):
        erg = []
        for i in range (1,self.getNumberOfRecords()+1):
            ergdic = {'author':'', 'title':'', 'source':'', 'timescited': 0}
            text = tostring(self.page.get_element_by_id('RECORD_%s'% str(i)))
            text = self.replaceAllHighlites(text)
            text = regexSuite['extrachars'].sub('',text)
            print text
            author = regexSuite['author'].search(text)
            if author != None:
                ergdic['author']=author.group(1)
            source = regexSuite['source'].search(text)
            if source != None:
                ergdic['source']=source.group(1)
            title = regexSuite['title'].search(text)
            if title != None:
                ergdic['title']=title.group(1)
            timescited = regexSuite['timescited'].search(text)
            if timescited != None:
                ergdic['timescited']=int(timescited.group(1))
            erg.append(ergdic)
        return erg

    def getISIScore(self):
        return len(self.ISIData)

def calcISIScoreWithArticles(authorname, titles):
    try:
        correctTitles = [title.rstrip(".?!") for title in titles]
        return sum([IsiHandler(convertScholarNameToISIName(authorname),title).getISIScore() for title in correctTitles])
    except:
        print "well, that didn't work <(','<) <(',')> (>',')>"
        return 0

def calcISIScore(authorname):
    """get number of articles on isi"""
    pass

def refreshArticles(article):
    """fetch number of cites for articles and add missing information (like source, datatype...)"""
    #TODO implement
    article.times_cited_on_isi = 2;
    article.save()

def convertScholarNameToISIName(name):
    return ' '.join(name.split(' ')[::-1])

if __name__ == '__main__':
    print calcISIScore('D Cass',['Do sunspots matter?'])

