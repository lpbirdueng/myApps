#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib import request
from urllib.error import URLError, HTTPError
import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from urllib.parse import urljoin
import csv
import time
from datetime import datetime
import lxml.html
from lxml.cssselect import CSSSelector
#import robotparser
#import Queue

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w',newline=''),quoting = csv.QUOTE_MINIMAL)
        self.fields = ('area','population','iso','country','capital','continent','tld','currency_code','currency_name','phone','postal_code_format','postal_code_regex','languages','neighbours')
        self.writer.writerow(self.fields)
        
    def __call__(self,url,html):
        if re.search('view/',url):
            tree = lxml.html.fromstring(str(html))
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table >tr#places_{}__row >td.w2p_fw'.format(field))[0].text_content())
                self.writer.writerow(row)
    
def link_crawler(seed_url, link_regex, scrape_callback=None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        links = []
        if scrape_callback:
            links.extend(scrape_callback(url,html) or [])
        if link_regex:
            #filter for links matching our regualr expression
            links.extend(link for link in get_links(html) if re.match(link_regex, link))
        
        for link in links:
            link = normalize(seed_url, link)
            #check whether already crawled this link
            if link not in seen:
                seen.add(link)
                #check link is within same domain
                if same_domain(seed_url, link):
                    crawl_queue.append(link)
    print("crawl_queue = ",crawl_queue)
    
"""
            for link in get_links(html):
                if re.match(link_regex, link):
                    # form absolute link
                    link = urlparse.urljoin(seed_url,link)
                    # check if have already seen this link
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
"""
def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link,_= urldefrag(link) #remove hash to avoid duplicates
    return urljoin(seed_url, link)

def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse(url1).netloc == urlparse(url2).netloc

def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(str(html))

def download(url, user_agent='Mozilla/5.0', proxy='http://luale:ZAQ!5tgb@mwghkg.corp.knorr-bremse.com:8080/wpad.dat', num_retries = 2):
    opener = request.build_opener()
    if proxy:
        proxy_handler = request.ProxyHandler({'http': proxy})
        opener.add_handler(proxy_handler)
    headers = [('User-agent', user_agent)]
    opener.addheaders = headers
    
    print("Downloading:", url)
    try:
        with opener.open(url) as f:
            html = f.read()
    except URLError as e:
        print("Download URL Error:", e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code <600:
                # retry 5xx HTTP errors
                return download(url, user_agent, number_retries - 1)
    return html

def crawl_sitemap(url):
    #download the sitemap file
    sitemap = download(url)
    #extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', str(sitemap))
    #links = re.match('<loc>(.*?)</loc>', sitemap)
    #download each link
    for link in links:
        html = download(link)
        print(link)

if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', scrape_callback=ScrapeCallback())

    
"""
def downloadHtml(url):
    proxy_handler = request.ProxyHandler({'http': 'http://luale:ZAQ!4rfv@mwghkg.corp.knorr-bremse.com:8080/wpad.dat'})
    #proxy_auth_handler = request.ProxyBasicAuthHandler()
    #proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
    opener = request.build_opener(proxy_handler)
    print('Downloading:', url)
    try:
        with opener.open(url) as f:
            html = f.read()
    except HTTPError as e:
        print("Download Http Error:", e.code, " ", e.reason)
        html = None
    except URLError as e:
        print("Download URL Error:", e.code, " ", e.reason)
        html = None
    return html
"""