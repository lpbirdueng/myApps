import urllib
import random
import time
from datetime import datetime
import socket
from urllib.parse import urlparse
from urllib.request import Request
from zipfile import ZipFile
import zipfile
from io import BytesIO
import logging
from Common import constants
from Common import web_utility
import http.cookiejar
import re
import queue

DEFAULT_AGENT = \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
# DEFAULT_DELAY = 5
DEFAULT_DELAY = random.randint(2, 6)
DEFAULT_RETRIES = 10
DEFAULT_TIMEOUT = 6000
# DEFAULT_PROXIES = 'http://luale:ZAQ!5tgb@mwghkg.corp.knorr-bremse.com:8080/wpad.dat'
DEFAULT_PROXIES = constants.cProxy


class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=DEFAULT_PROXIES,
                 num_retries=DEFAULT_RETRIES, timeout=DEFAULT_TIMEOUT, opener=None, cache=None, data=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache
        self.data = data
        if opener is None:
            cj = http.cookiejar.CookieJar()
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        else:
            self.opener = opener

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignor result from cache and re-download
                    result = None

        if result is None:
            # result was not loaded from cache so still need to download
            self.throttle.wait(url)
            # proxy = random.choice(self.proxies) if self.proxies else None
            proxy = self.proxies if self.proxies else None
            headers = {'user-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries, data=self.data)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        if data is not None:
            encoded_data = urllib.parse.urlencode(data)
            encoded_data = encoded_data.encode('utf-8')
        else:
            encoded_data = None
        print('Downloading:', url, ' ', encoded_data)
        request = urllib.request.Request(url, encoded_data, headers or {})
        # opener = self.opener or request.build_opener()
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            proxy_params = {urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
            logging.basicConfig(filename='download.log', level=logging.DEBUG)
            logging.info('%s,%s,%s', code, url, data)
        except Exception as e:
            print('Download error:', str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # retry 5XX HTTP errors
                    # return self._get(url, headers, proxy, num_retries - 1, data)
                    return self.download(url, headers, proxy, num_retries, data)
                else:
                    logging.basicConfig(filename='download.log', level=logging.ERROR)
                    logging.error('%s,%s,%s', code, str(e), url)
            else:
                code = None
                logging.basicConfig(filename='download.log', level=logging.ERROR)
                logging.error('Error,%s', url)
        return {'html': html, 'code': code}

    def saveZipToLocal(self, url, filename='test.zip', extract=False, path='./download'):
        zipped_data = self.__call__(url)
        if len(zipped_data) == 0:
            return False
        if extract:
            try:
                with ZipFile(BytesIO(zipped_data)) as zf:
                    if path is not None:
                        zf.extractall(path=path)
                    else:
                        zf.extractall()
            except zipfile.BadZipFile:
                print("Bad Zip file, retry", self.data)
                print(zipped_data)
                logging.basicConfig(filename='download.log', level=logging.ERROR)
                logging.error('Bad Zip,%s', self.data)
                # return self.saveZipToLocal(url, filename, extract)
                return False
        else:
            with open(filename, "wb") as f:
                f.write(zipped_data)
        return True

    def crawl_sitemap(self, sitemap_url):
        # download the sitemap file
        # sitemap = self.download(url=sitemap_url, proxy=proxy, headers=headers, num_retries=self.num_retries)
        sitemap = self.__call__(sitemap_url)
        # extract the sitemap links
        links = re.findall(r'<loc>(.*?)</loc>', sitemap)
        for link in links:
            # html = self.download(url=link, proxy=proxy, headers=headers, num_retries=self.num_retries)
            html = self.__call__(url=link)
            # scrape html here

    def link_crawler(self, seed_url, link_regex=None, delay=DEFAULT_DELAY, max_depth=-1, max_urls=-1,
                     scrape_callback=None):
        """Crawl from the given seed URL following links matched by link_regex"""
        # the queue of URL's that still need to be crawled
        crawl_queue = queue.deque([seed_url])
        # the URL's that have been seen and at what depth
        seen = {seed_url: 0}
        # track how many URL's have been downloaded
        num_urls = 0
        rp = web_utility.get_robots(seed_url)
        throttle = Throttle(delay)
        # proxy = self.proxies if self.proxies else None
        # headers = {"user-agent": self.user_agent}

        while crawl_queue:
            url = crawl_queue.pop()
            # check url passes robots.txt restrictions
            if rp.can_fetch(self.user_agent, url):
                throttle.wait(url)
                # html = self.download(url, headers=headers, proxy=proxy, num_retries=self.num_retries)['html']
                html = self.__call__(url)
                html_str = html.decode('utf-8')
                links = []
                if scrape_callback:
                    links.extend(scrape_callback(url, html_str) or [])
                depth = seen[url]
                if depth != max_depth:
                    # can still crawl further
                    if link_regex:
                        # filter for links matching our regualar expression
                        links.extend(link for link in web_utility.get_links(html_str) if re.match(link_regex, link))

                    for link in links:
                        link = web_utility.normalize(seed_url, link)
                        # check whether already crawled this link
                        if link not in seen:
                            seen[link] = depth + 1
                            # check link is within same domain
                            if web_utility.same_domain(seed_url, link):
                                # success! add this new link to queue
                                crawl_queue.append(link)
                # check whether have reached downloaded maximum
                num_urls += 1
                if num_urls == max_urls:
                    break
            else:
                print("Blocked by robots.txt:", url)

    def login_cookies(self, url, data={}):
        if data is not None:
            encoded_data = urllib.parse.urlencode(data)
            encoded_data = encoded_data.encode('utf-8')
        else:
            encoded_data = None

        proxy = self.proxies if self.proxies else None
        headers = {'user-agent': self.user_agent}
        request = urllib.request.Request(url, encoded_data, headers or {})
        # cj = http.cookiejar.CookieJar()
        # opener = self.opener or urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        # opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener = self.opener
        if proxy:
            proxy_params = {urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
            print(response.geturl())
            logging.basicConfig(filename='download.log', level=logging.DEBUG)
            logging.info('Sign in info: %s,%s,%s', code, url, data)
        except Exception as e:
            print('Sign in error:', str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                logging.basicConfig(filename='download.log', level=logging.ERROR)
                logging.error('Sign in error: %s,%s,%s', code, str(e), url)
            else:
                code = None
                logging.basicConfig(filename='download.log', level=logging.ERROR)
                logging.error('Sign in Error,%s', url)
        return opener


class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        """Delay if have accessed this domain recently
        """
        domain = urllib.parse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay + random.uniform(0, 2) - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()
