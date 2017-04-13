from Common.downloader import Downloader
D = Downloader()
url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
values={
    'K_code' : '',
    'market' : 'sz',
    'type' : 'lrb',
    'code' : '000001',
    'orgid' : 'gssz000001',
    'minYear' : '1991',
    'maxYear' : '2017',
    'hq_code' : '',
    'hq_k_code' : '',
    'cw_code' : '000001',
    'cw_k_code' : ''
}
D.data = values
D.saveZipToLocal(url,extract=True)

"""
url='http://www.cninfo.com.cn/cninfo-new/data/query'
values = {'keyWord' : '000001',
          'maxNum' : '9999',
          'hq_or_cw' : '2' }
D.data = values
result = D(url)
print(result)
"""