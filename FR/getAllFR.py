from FR import frDownloader
from FR import stockCode

if __name__ == '__main__':
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    frDownloader.getFR(url=url,stock_list=stockCode.szStockList)