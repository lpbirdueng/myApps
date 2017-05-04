# -*- coding: utf-8 -*-

import csv
import re
import lxml.html
from Common import downloader


class ScrapeCallback:
    def __init__(self, filename="result.csv"):
        self.filename = filename
        self.writer = csv.writer(open(self.filename, 'w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search(r'/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)


if __name__ == '__main__':
    D = downloader.Downloader()
    D.link_crawler('http://example.webscraping.com/', r'/(index|view)', scrape_callback=ScrapeCallback())
