import os
import json
import feedparser
import urllib
from urllib2 import urlopen
import HTMLParser
import clientSQL

# figure out what dir we are in (needed to load other files when deploying to a server)
basedir = os.path.dirname(os.path.abspath(__file__))

# read in mapping of country names to paths to RSS feeds on the Global Voices server
f = open(basedir+'/globalvoices-countrypaths.json', 'r')
path_lookup = json.loads(f.read())


def recent_stories_from(country , repeatStory):
    '''
    Return a list of the last 3 stories for a given country
    '''
    h = HTMLParser.HTMLParser()
    #raw_content = urlopen( _content_url_via_google_for( country , repeatStory) ).read()
    if country == "Spain" or country =="France" or country == "Germany" or country == "Italy":
        json_file = '{"responseData": {"feed":{"feedUrl":"http://globalvoicesonline.org/-/world/east-asia/cambodia/feed","title":"Global Voices Cambodia","link":"http://globalvoicesonline.org","author":"","description":"Citizen media stories from around the world","type":"rss20","entries":[{"title":"Hands on Foundation Class","link":"https://docs.google.com/document/d/1A7NUoLr0jvPTBSSwwHuvW7YAy8CHKLrU-wrHCYfSe28/edit/","author":"Xavier Benavides","publishedDate":"Thu, 06 Nov 2014 17:20:16 -0800","contentSnippet":"The goal of this module is to introduce you to an overview of software development methodologies to help you succeed in your time at the Media Lab...","content":" " ,"categories":["Cambodia","East Asia","Economics Business","English","Environment","Indigenous","International Relations","Laos","Quick Reads"]}]}}, "responseDetails": null, "responseStatus": 200}'
        
        #Insert post of differents countries in the DB
        aux1 = clientSQL.sqlInsert()

        ##Extract the post of a country
        aux2 = clientSQL.sqlPop(country)

        #Upload the Info in the HTML file
        content = json.loads( json_file )
        stories = []

        for details in content['responseData']['feed']['entries']:
            stories.append( {
            'title': aux2['title'],
            'link': aux2['link'],
            'author': aux2['author'],
            'contentSnippet': h.unescape(aux2['contentSnippet'])
            } )
        return stories

    else:
        raw_content = urlopen( _content_url_via_google_for( country , repeatStory) ).read()
        json_file = '{"responseData": {"feed":{"feedUrl":"http://globalvoicesonline.org/-/world/east-asia/cambodia/feed","title":"Global Voices Cambodia","link":"http://globalvoicesonline.org","author":"","description":"Citizen media stories from around the world","type":"rss20","entries":[{"title":"NOT IN THE DB","link":"https://docs.google.com/document/d/1A7NUoLr0jvPTBSSwwHuvW7YAy8CHKLrU-wrHCYfSe28/edit/","author":"Xavier Benavides","publishedDate":"Thu, 06 Nov 2014 17:20:16 -0800","contentSnippet":"Included in the DB: Spain, Germany, Italy and France","content":" " ,"categories":["Cambodia","East Asia","Economics Business","English","Environment","Indigenous","International Relations","Laos","Quick Reads"]}]}}, "responseDetails": null, "responseStatus": 200}'
        content = json.loads( json_file )
        stories = []

        for details in content['responseData']['feed']['entries']:
            stories.append( {
            'title': details['title'],
            'link': details['link'],
            'author': details['author'],
            'contentSnippet': h.unescape(details['contentSnippet'])
            } )
        return stories
   

def country_list():
    '''
    Return a list of all the countries with feeds on the Global Voices site
    '''
    return path_lookup.keys()

def _content_url_via_google_for(country , repeatStory):
    '''
    Return the URL to the RSS content for a country via the Google API, so we can get in JSON directly 
    (rather than in XML)
    '''
    return "http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num="+str(repeatStory)+"&q="+ urllib.quote( _rss_url_for(country).encode("utf-8") )

def _rss_url_for(country):
    '''
    Return the URL to the RSS feed of stories for a country
    '''
    return "http://globalvoicesonline.org" + path_lookup[country] + "feed";
