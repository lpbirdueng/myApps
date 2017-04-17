# -*- coding: utf-8 -*-
import lxml.html


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
