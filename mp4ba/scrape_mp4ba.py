# -*- coding: utf-8 -*-
from Common import downloader
import lxml.html
import re
from Common import mongodb_utility
import csv
import pandas as pd
from pandas import DataFrame


class MP4ba_Scrapecallback:
    def __init__(self, filename = "result.csv"):
        self.filename = filename
        self.writer = csv.writer(open(self.filename, 'w'))
        self.fields = ('title', 'update info', 'image', 'text', 'play_link', 'BT_Seed', 'Baidu Pan', 'source')
        self.writer.writerow(self.fields)


    def __call__(self, url, html):
        if re.search(r'/mp4/hd', url):
            tree = lxml.html.fromstring(html)
            row = []
            #df = DataFrame(columns=self.fields)
            text = ""
            for field in self.fields:
                if field == 'title':
                    title = tree.cssselect('div.newscon > h1')
                    if len(title)>0:
                        title_text = title[0].text_content()
                        #print("title =", title)
                    else:
                        title_text = "null"
                    row.append(title_text)
                    continue
                if field == 'update info':
                    update_info = tree.cssselect('div.newscon > span.info')
                    if len(update_info)>0:
                        update_info_text = update_info[0].text_content()
                        #print("Update = ", update_info)
                    else:
                        update_info_text = "null"
                    row.append(update_info_text)

                    continue
                if field == 'image':
                    image_link = tree.cssselect('div#text > img:first-of-type')
                    if len(image_link)>0:
                        image_link_text = image_link[0].attrib['src']
                        #print("image link = ", image_link)
                    else:
                        image_link_text = "null"
                    row.append(image_link_text)
                    continue
                if field == 'text':
                    text_contents = tree.cssselect('div#text > div:not(.newslist10)')
                    for line in text_contents:
                        text = text + ";" + line.text_content()
                    #print("text content = ", text)
                    row.append(text)
                    continue
                if field == 'play_link':
                    play_link = tree.cssselect('iframe')
                    if len(play_link)>0:
                        play_link_src = play_link[0].attrib['src']
                        #print("play link = ", play_link)
                    else:
                        play_link_src = "null"
                    row.append(play_link_src)
                    #row.append(tree.cssselect('div.newslist10 > li > table > tbody > tr > td > iframe')[0].attrib.get['src'])
                    continue
                if field == 'BT_Seed':
                    BT_link = tree.cssselect('span > a[href$=".torrent"]')
                    if len(BT_link) > 0:
                        BT_link_text = BT_link[0].attrib['href']
                    else:
                        BT_link_text = "null"
                    row.append(BT_link_text)
                    #print("bt link = ", BT_link)
                    continue
                if field == 'Baidu Pan':
                    baidupan = tree.cssselect('span > a[href*="pan.baidu.com"]')
                    if len(baidupan) > 0:
                        baidupan_text = baidupan[0].text_content()
                    else:
                        baidupan_text = "null"
                    #print("baidupan = ", baidupan)
                    row.append(baidupan_text)
                    continue
                if field == 'source':
                    row.append(url)
                #row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)

if __name__ == '__main__':
    D = downloader.Downloader()
    #url = "http://www.mp4pa.com/mp4/hd5655.html"
    #html = D(url)
    #print(html)
    #SC = MP4ba_Scrapecallback()
    #SC(url, html)
    D.link_crawler('http://www.mp4pa.com', r'/(mp4|dy|top)', scrape_callback=MP4ba_Scrapecallback())
