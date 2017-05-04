# -*- coding: utf-8 -*-
import lxml.html
from urllib.parse import urlparse
from urllib import parse
from urllib import robotparser
import re


def parse_form(html):
    """extract all input properties from the form
    :param html: webpage source code
    :return: dictionary which contain all the input field
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def normalize(seed_url, link):
    """  Normalize this URL by removing hash and adding domain"""
    link, _ = parse.urldefrag(link)  # remove hash to avoid duplicates
    return parse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain"""
    return urlparse(url1).netloc == urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain"""
    rp = robotparser.RobotFileParser()
    rp.set_url(parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html"""
    # a regualar expression to extract all links from the webpage
    webpage_regex = re.compile(r'<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)
