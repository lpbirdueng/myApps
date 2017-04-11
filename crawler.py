from urllib import request
from Common.downloader import Downloader
from zipfile import ZipFile
from io import BytesIO
import io
import csv

D = Downloader()
result = D('http://www.csindex.com.cn/sseportal/ps/zhs/hqjt/csi/show_zsgz.js')
decoded_result = result.decode('gbk')
f = open('test.txt', 'w')
f.write(str(decoded_result))
f.close
#zipped_data = D.saveZipToLocal(url = 'http://115.29.204.48/syl/20170315.zip', filename='20170315.zip',extract=True)

"""
zipped_data = D(url = 'http://115.29.204.48/syl/20170315.zip')
print(type(zipped_data))
f = open("t.zip","w+b")
f.write(zipped_data)
f.close


with ZipFile(BytesIO(zipped_data)) as zf:
    csv_filename = zf.namelist()[0]
    data = zf.open(csv_filename).read()
    f = open('test.xls', 'w+b')
    f.write(data)
    f.close
"""
    #decoded_data = data.decode('utf-32','backslashreplace')
    #zf.extractall()