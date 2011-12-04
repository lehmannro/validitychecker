Climate Goggles
===============
-- protect your brain from climate fiction

## How to use
### Dependencies
* [Python 2.7](http://python.org/)
* [Django](https://www.djangoproject.com/)
* [Beautiful soup](http://www.crummy.com/software/BeautifulSoup/)
* [lxml](http://lxml.de/)
* [SQLite](http://www.sqlite.org/)


### Installation
Just in case you have no idea how to get going here are the required commands for Ubuntu:
    
    git clone git@github.com:lehmannro/validitychecker.git
    sudo apt-get install python python-pip python-dev sqlite3
    sudo pip install django
    sudo pip install beautifulsoup
    sudo pip install lxml
    cd validitychecker/www/
    python manage.py syncdb --noinput
    python manage.py runserver


## Problem
* It is difficult for normal people to classify the background of scientific statements and what is serious. 
* Climate change is a very complex subject with a  lot of misinformation circulating. 
* This misinformation creates uncertainty. 
* Some incorrect information is scattered by climate skeptics, with the aim to sow doubt and ultimately to prevent climate protection.
* [Problem definition](http://www.rhok.org/problems/validity-detectorchecker-aggregation-and-validation-statements-about-climate-change-deen)

## Challenges
* Sorting and ranking scientific papers is hard
* Scientific papers are written in technical language
* Few resources provide proper APIs

## Solution
* User enters search query
* Lookup on Google Scholar
* Match the authors against ISI
* Compute a score for the authors
* Find easy-to-read resources of the author

## User expierience
* The user experience is designed to be simple

* Seamless browser integration with Greasemonkey script
* Available in English and German
* Adaptive Design for smaller screen sizes

## Remaining issues
* Register for the ISI Web of Knowledge API and implement the hooks
* Digestible article summaries 

## Team
### Backend
* [Robert Lehmann](https://github.com/lehmannro/)
* [Dominik Moritz](https://github.com/domoritz/)
* [André Rieck](https://github.com/Varek/)
* [Thomas Werkmeister](https://github.com/lesnail/)
### Frontend
* [David Owens](https://github.com/fineartdavid/)
* [Norman Rzepka](https://github.com/normanrz/)
### Design
* [Milena Glim](https://github.com/milenskaya/)

## Stuff we used
* [Google Scholar](http://scholar.google.com/)
* [ISI Web Knowledge](http://apps.isiknowledge.com/)
* [Arvo Font](http://www.fontsquirrel.com/fonts/arvo)



