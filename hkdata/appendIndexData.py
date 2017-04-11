#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from myApps import crawler_tools
from datetime import timedelta
from datetime import date
from datetime import datetime
from tools import removeheader

def getlastdate(filename=''):
    #f = open(filename, 'r',encoding = 'utf-16', newline='')
    #text = f.read()
    with open(filename, 'r',encoding = 'utf-16', newline='') as f:
        text = f.read()
    rows = text.split('\n')
    #Get last row of the list
    for i in range(len(rows)):
        if rows[-1-i] == '':
            continue
        else:
            last_row = rows[-1-i].split('\t')
            break    
    last_date = date(int(last_row[0][0:4]),int(last_row[0][4:6]),int(last_row[0][6:8]))
    #last_date = datetime.strptime(last_row[0],'%Y%m%d')
    return last_date
def appenddata(url='', filename=''):
    data = crawler_tools.download(url)
    if data:
        decoded_data = data.decode('utf-16','backslashreplace')
        decoded_data = decoded_data.replace('\"',"")
        print('decoded_data=',decoded_data)
        lines = decoded_data.split('\n')
        items = removeheader(lines, 2)
        #append data to file
        for item in items:
            if item =='':
                continue
            with open(filename, 'a',encoding = 'utf-16', newline='\n') as f:
                f.write(item+'\n')
            #f = open(filename, 'a', encoding = 'utf-16', newline='')
            #f.write(item)
            #f.close()
def appendIndexData(url_prefix='',filename=''):
    today = date.today()
    # 1 day
    single_day = timedelta(days=1)
    next_date = getlastdate(filename) + single_day
    while True:
        if next_date<today:
            date_str = str(next_date.strftime('%d%b%y'))
            if date_str[0] == '0':
                date_str =  date_str[1:]
            url=url_prefix + date_str + '.csv'
            appenddata(url,filename)
            next_date = next_date + single_day
        else:
            exit()    
