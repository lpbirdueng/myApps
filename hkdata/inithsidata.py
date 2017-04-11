from initdata import initindexdata
hsi_url_prefix = 'http://sc.hangseng.com/gb/www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hsi/idx_'
filename = 'hsi_rawdata_temp.csv'
initindexdata(hsi_url_prefix, filename)

'''
f = open(filename, 'r',encoding = 'utf-16')
text = f.read()
items = text.split('\n')
for item in items:
    if item =='':
        print('item=',item)
'''