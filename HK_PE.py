#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from crawler_tools import download
import re
#url = 'http://sc.hangseng.com/gb/www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hscei/idx_10Mar17.csv'
url = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hscei/idx_10Mar17.csv'
data = download(url)
text = data.decode('utf-16','backslashreplace')
rows = text.split("\n")
last_row = re.findall(r'"(.*?)"\s+',rows[2])
f = open('rawdata.csv', 'w', encoding = 'utf-16', newline='')
print(rows[2])
f.write(text)
f.close()
