import urllib
#import random
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
DEFAULT_AGENT = 'Mozilla/5.0'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 10
DEFAULT_TIMEOUT = 600
#DEFAULT_PROXIES = 'http://luale:ZAQ!5tgb@mwghkg.corp.knorr-bremse.com:8080/wpad.dat'
DEFAULT_PROXIES = constants.cProxy

class Downloader:
    def __init__(self, delay=DEFAULT_DELAY,user_agent=DEFAULT_AGENT, proxies=DEFAULT_PROXIES,num_retries=DEFAULT_RETRIES,timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache
    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                #url is not available in cache
                pass
            else:                
                if self.num_retries > 0 and 500<=result['code']<600:
                    #server error so ignor result from cache and re-download
                    result = None
                
        if result is None:
            #result was not loaded from cache so still need to download
            self.throttle.wait(url)
            #proxy = random.choice(self.proxies) if self.proxies else None
            proxy = self.proxies if self.proxies else None
            headers={'user-agent':self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                #save result to cache
                self.cache[url] = result
        return result['html']
    
    def download(self, url, headers, proxy, num_retries, data=None):
        print('Downloading:',url)
        request = urllib.request.Request(url, data, headers or {})
        #opener = self.opener or request.build_opener()
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            proxy_params = {urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
            logging.basicConfig(filename='download.log',level=logging.DEBUG)
            logging.info('%s,%s',code,url)
        except Exception as e:
            print('Download error:',str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # retry 5XX HTTP errors
                    return self._get(url, headers, proxy, num_retries-1, data)
                else:
                    logging.basicConfig(filename='download.log',level=logging.ERROR)
                    logging.error('%s,%s,%s',code,str(e),url)
            else:
                code = None
                logging.basicConfig(filename='download.log',level=logging.ERROR)
                logging.error('Error,%s',url)
        return {'html': html, 'code': code}
    
    def saveZipToLocal(self, url, filename='test.zip',extract=False):
        zipped_data = self.__call__(url)
        if (len(zipped_data) == 0):
            return False
        if extract:
            try:
                with ZipFile(BytesIO(zipped_data)) as zf:
                    zf.extractall()
            except zipfile.BadZipFile:
                print("Bad Zip file, retry")
                #return self._get(url,filename,extract)
                return self.saveZipToLocal(url,filename,extract)                
        else:
            f = open(filename,"w+b")
            f.write(zipped_data)
            f.close
        return True
    
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
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()