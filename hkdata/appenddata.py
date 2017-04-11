#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myApps import crawler_tools
from datetime import timedelta
from datetime import date
from datetime import datetime
#Define file name with absolute path for task scheduler convienience
filename = 'C:\\Users\\luale\\Documents\\alex\\software\\py\\myApps\\hkdata\\rawdata_temp.csv'
#filename = 'rawdata_temp.csv'
url_prefix = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hscei/idx_'

def getlastdate():
    f = open(filename, 'r',encoding = 'utf-16',newline='')
    text = f.read()
    rows = text.split('\n')
    last_row = rows[-2].split('\t')
    print('text=',text)
    
    last_date = date(int(last_row[0][0:4]),int(last_row[0][4:6]),int(last_row[0][6:8]))
    print(last_row[0])
    #last_date = datetime.strptime(last_row[0],'%Y%m%d')
    print("last date:", last_date)
    return last_date
def appenddata(url=''):
    data = crawler_tools.download(url)
    if data:
        decoded_data = data.decode('utf-16','backslashreplace')
        lines = decoded_data.split('\n')
        append_data = lines[2]
        #append data to file
        f = open(filename, 'a', encoding = 'utf-16', newline='')
        f.write(append_data)
        f.close()
    
today = date.today()
# 1 day
single_day = timedelta(days=1)
next_date = getlastdate() + single_day
while True:
    if next_date<today:
        date_str = str(next_date.strftime('%d%b%y'))
        if date_str[0] == '0':
            date_str =  date_str[1:]
        url=url_prefix + date_str + '.csv'
        appenddata(url)
        next_date = next_date + single_day
    else:
        exit()    

