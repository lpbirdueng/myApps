import lxml.html
from Common.downloader import Downloader
import pprint
import urllib.parse
import urllib.request


LOGIN_URL = "http://example.webscraping.com/user/login"
LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'exampl'


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data
D = Downloader()

html = D(LOGIN_URL)

data = parse_form(html)
pprint.pprint(data)
data['email']=LOGIN_EMAIL
data['password']=LOGIN_PASSWORD
D.login_cookies(LOGIN_URL, data)

"""
proxy_support = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
req = urllib.request.Request(url=LOGIN_URL,data=encoded_data)
with urllib.request.urlopen(req) as response:
    html = response.read()
    #print(response.geturl())
"""
