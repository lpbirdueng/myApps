# -*- coding: utf-8 -*-
from Common import mongodb_utility
from FR import frDownloader


stock_list = (["600000", "1989", "2016"],
                ["600004", "2000", "2016"])
url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
# frDownloader.getFR(url=url,stock_list=stockCode.szStockList)
frDownloader.getFR(url=url, stock_list=stock_list)
"""
con = mongodb_utility.connect_db(db_name="list_company")
results = mongodb_utility.export2df(database=con,collection="sz_stock")
print(results)
"""