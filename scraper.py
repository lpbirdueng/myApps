from urllib import request
from urllib.error import URLError, HTTPError
import re
from urllib.parse import urlparse

def link_crawler(seed_url, link_regex):
    """Crawl from the given seed URL following links matched by link_regex
    """
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        #filter for links matching our regualr expression
        for link in get_links(html):
            if re.match(link_regex, link):
                # form absolute link
                link = urlparse.urljoin(seed_url,link)
                # check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)
                
def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

def download(url, user_agent='Mozilla/5.0', proxy='http://luale:ZAQ!4rfv@mwghkg.corp.knorr-bremse.com:8080/wpad.dat', num_retries = 2):
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
        #html = download(link)
        print(link)

#data = downloadHtml('http://example.webscraping.com/sitemap.xml')
data = download('http://example.webscraping.com/sitemap.xml')
print(data)
#crawl_sitemap('http://example.webscraping.com/sitemap.xml')

#with request.urlopen('http://api.douban.com/v2/book/2129650') as f:
#    data = f.read()
#    #print('Status:', f.status, f.reason)
#    print(data)
    
""""
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
""""