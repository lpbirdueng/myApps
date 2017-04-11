from appendIndexData import appendIndexData
#Define file name with absolute path for task scheduler convienience
#filename = 'C:\\Users\\luale\\Documents\\alex\\software\\py\\myApps\\hkdata\\rawdata_temp.csv'
hsi_url_prefix = 'http://www.hsi.com.hk/HSI-Net/static/revamp/contents/en/indexes/report/hscei/idx_'
filename = 'hscei_rawdata_temp.csv'
appendIndexData(hsi_url_prefix, filename)