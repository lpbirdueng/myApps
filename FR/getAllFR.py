from FR import frDownloader
from FR import stockCode
from Common import mongodb_utility
from pandas import Series

def update_sh_b_data(update_year="2016"):
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    """get stock list"""
    db = mongodb_utility.connect_db(db_name="list_company")
    sh_df = mongodb_utility.export2df(database=db, collection="sh_stock")

    """download sh B stock data"""
    sh_df_b = sh_df[Series(sh_df['A股上市日期']).isnull()][["_id"]]
    sh_df_b["_id"] = sh_df_b["_id"].apply(lambda x: str(int(x)))
    sh_df_b["min_year"] = update_year
    sh_df_b["max_year"] = update_year
    shb_list = sh_df_b.values.tolist()
    frDownloader.getFR(url=url, stock_list=shb_list)

def update_sh_a_data(update_year="2016"):
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    """get stock list"""
    db = mongodb_utility.connect_db(db_name="list_company")
    #sz_df = mongodb_utility.export2df(database=db, collection="sz_stock")
    sh_df = mongodb_utility.export2df(database=db, collection="sh_stock")

    """download sh A stock data"""
    sh_df_a = sh_df[Series(sh_df['A股上市日期']).notnull()][["_id"]]
    sh_df_a["_id"] = sh_df_a["_id"].apply(lambda x: str(int(x)))
    sh_df_a["min_year"] = update_year
    sh_df_a["max_year"] = update_year
    sha_list = sh_df_a.values.tolist()
    frDownloader.getFR(url=url, stock_list=sha_list)

def update_sz_b_data(update_year="2016"):
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    """get stock list"""
    db = mongodb_utility.connect_db(db_name="list_company")
    sz_df = mongodb_utility.export2df(database=db, collection="sz_stock")

    """download sz B stock data"""
    sz_df_b = sz_df[Series(sz_df['A股上市日期']).isnull()][["_id"]]
    sz_df_b["_id"] = sz_df_b["_id"].apply(lambda x: str(int(x)))
    sz_df_b["min_year"] = update_year
    sz_df_b["max_year"] = update_year
    szb_list = sz_df_b.values.tolist()
    frDownloader.getFR(url=url, stock_list=szb_list)

def update_sz_a_data(update_year="2016"):
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    """get stock list"""
    db = mongodb_utility.connect_db(db_name="list_company")
    sz_df = mongodb_utility.export2df(database=db, collection="sz_stock")

    """download sz A stock data"""
    sz_df_a = sz_df[Series(sz_df['A股上市日期']).notnull()][["_id"]]
    sz_df_a["_id"] = sz_df_a["_id"].apply(lambda x: str(int(x)))
    sz_df_a["min_year"] = update_year
    sz_df_a["max_year"] = update_year
    sza_list = sz_df_a.values.tolist()
    frDownloader.getFR(url=url, stock_list=sza_list)

if __name__ == '__main__':
    update_sh_b_data(update_year="2016")
    """
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    db = mongodb_utility.connect_db(db_name="list_company")
    sz_df = mongodb_utility.export2df(database=db,collection="sz_stock")
    sh_df = mongodb_utility.export2df(database=db,collection="sh_stock")
    """
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
    """download SH B stock data"""
    """
    df_b = sh_df[Series(sh_df['A股上市日期']).isnull()][["_id", "B股上市日期"]]
    df_b["B股上市日期"] = df_b["B股上市日期"].apply(lambda x: str(x.strip())[0:4])
    df_b["_id"] = df_b["_id"].apply(lambda x: str(int(x)))
    df_b["max_year"] = "2016"
    shb_list = df_b.values.tolist()
    print(shb_list)
    frDownloader.getFR(url=url, stock_list=shb_list)
    """
    #frDownloader.get_fixed_year(url=url,stock_list=sz_list,max_year='2017')
    #frDownloader.getFR(url=url,stock_list=stockCode.szStockList)
    #frDownloader.getFR(url=url, stock_list=stockCode.shastocklist)