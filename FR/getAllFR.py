from FR import frDownloader
from FR import stockCode
from Common import mongodb_utility
from pandas import Series

if __name__ == '__main__':
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    db = mongodb_utility.connect_db(db_name="list_company")
    sz_df = mongodb_utility.export2df(database=db,collection="sz_stock")
    sh_df = mongodb_utility.export2df(database=db,collection="sh_stock")
    """
    df = sz_df[Series(sz_df['A股上市日期']).notnull()][["_id", "A股上市日期"]]
    df["A股上市日期"] = df["A股上市日期"].apply(lambda x: str(x)[0:4])
    df["max_year"] = "2016"
    """
    """download SZ B stock data
    """
    """
    df_b = sz_df[Series(sz_df['A股上市日期']).isnull()][["_id", "B股上市日期"]]
    df_b["B股上市日期"] = df_b["B股上市日期"].apply(lambda x: str(x.strip())[0:4])
    df_b["_id"] = df_b["_id"].apply(lambda x: str(int(x)))
    df_b["max_year"] = "2016"
    szb_list = df_b.values.tolist()
    frDownloader.getFR(url=url, stock_list=szb_list)
    """
    """download SH B stock data
    """
    df_b = sh_df[Series(sh_df['A股上市日期']).isnull()][["_id", "B股上市日期"]]
    df_b["B股上市日期"] = df_b["B股上市日期"].apply(lambda x: str(x.strip())[0:4])
    df_b["_id"] = df_b["_id"].apply(lambda x: str(int(x)))
    df_b["max_year"] = "2016"
    shb_list = df_b.values.tolist()
    print(shb_list)
    frDownloader.getFR(url=url, stock_list=shb_list)

    #frDownloader.get_fixed_year(url=url,stock_list=sz_list,max_year='2017')
    #frDownloader.getFR(url=url,stock_list=stockCode.szStockList)
    #frDownloader.getFR(url=url, stock_list=stockCode.shastocklist)