#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myApps.Common.downloader import Downloader
import openpyxl
D = Downloader()
result = D('http://www.csindex.com.cn/sseportal/ps/zhs/hqjt/csi/show_zsgz.js')
decoded_result = result.decode('gbk').replace('var ','')
decoded_result = decoded_result.replace('"','')
result_lists = decoded_result.split('\r\n')
d = {}
for row in result_lists:
    if len(row) == 0:
        continue
    e = row.split('=')
    d[e[0]]=e[1]
count_str = ''
line_str = None
for r in range(11):
    line_str = d['zsgz00']
    for e in range(9):
        count_str = 'zsgz' + str(r+1) + str(e)
        line_str = line_str + '\t' + d[count_str]
    line_str= line_str + '\r\n'
    print(line_str)
    with open('indexvalue_temp.txt', 'a', encoding = 'utf-8', newline='') as f:
        f.write(line_str)
        