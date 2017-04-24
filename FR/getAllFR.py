from FR import frDownloader
from FR import stockCode
from Common import mongodb_utility
from pandas import Series

if __name__ == '__main__':
    db = mongodb_utility.connect_db(db_name="list_company")
    sz_df = mongodb_utility.export2df(database=db,collection="sz_stock")
    sh_df = mongodb_utility.export2df(database=db,collection="sh_stock")
    sz_list = list(sz_df[Series(sz_df['A股上市日期']).notnull()]["_id"])
    sh_list = list(sh_df['_id'])
    szb_list = list(sz_df[Series(sz_df['B股上市日期']).notnull()]['B股代码'])
    #print(sz_list)
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    #frDownloader.get_fixed_year(url=url,stock_list=sz_list,max_year='2017')
    #frDownloader.getFR(url=url,stock_list=stockCode.szStockList)
    #frDownloader.getFR(url=url, stock_list=stockCode.shastocklist)