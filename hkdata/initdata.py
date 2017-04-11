from myApps import crawler_tools
from datetime import timedelta
from datetime import date
#file_name = 'hsi_rawdata_temp.csv'
hsi_url_prefix = 'http://sc.hangseng.com/gb/www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hsi/idx_'
def removeheader(lines=[], n = 1):
    for i in range(n):
        lines.pop(n-1-i)
    return lines
def initdata(url='', file_name=''):
    data = crawler_tools.download(url)
    if data:
        decoded_data = data.decode('utf-16','backslashreplace')
        decoded_data = decoded_data.replace('\"',"")
        rows = decoded_data.split('\n')
        #remove header, first two lines
        items=removeheader(rows,2)
        #append data to file
        for item in items:
            if item =='':
                continue
            f = open(file_name, 'a', encoding = 'utf-16', newline='\n')
            f.write(item+'\n')
            f.close()
        return True
    else:
        return False    
    
def initindexdata(url_prefix='',filename=''):
    single_day = timedelta(days=1)
    current_date = date.today() - single_day
    num_retries = 5
    while True:
        date_str = str(current_date.strftime('%d%b%y'))
        if date_str[0] == '0':
            date_str =  date_str[1:]
        url=url_prefix + date_str + '.csv'
        if initdata(url, filename):
            current_date = current_date - single_day
            num_retries = 5
        else:
            if num_retries <=0:
                print("Done till", current_date)
                exit()
            else:
                num_retries = num_retries -1
                current_date = current_date - single_day
                continue
                
#inithsidata('hsi_rawdata_temp.csv')

'''    
#HSCEI data
#url_prefix = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hscei/idx_'
#HSI Index data
url_prefix = 'http://sc.hangseng.com/gb/www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hsi/idx_'

single_day = timedelta(days=1)
current_date = date.today() - single_day
num_retries = 5
while True:
    date_str = str(current_date.strftime('%d%b%y'))
    if date_str[0] == '0':
        date_str =  date_str[1:]
    url=hsi_url_prefix + date_str + '.csv'
    if initdata(url):
        current_date = current_date - single_day
        num_retries = 5
    else:
        if num_retries <=0:
            print("Done till", current_date)
            exit()
        else:
            num_retries = num_retries -1
            current_date = current_date - single_day
            continue
'''    