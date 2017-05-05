# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import json
from Common import file_util
import re
import os
import csv
from Common import mongodb_utility
from FR import frDownloader


def initimportdb(path, expression, dbhost="localhost", dbport=27017):
    file_list = file_util.get_file_list_with_filter(path=path, expression=expression)
    print("file number = ", len(file_list))
    if file_list is None:
        print("No file selected!")
        return None
    id_list = []
    re_table = re.compile(".*_(lrb|fzb|llb)_.*")
    client = MongoClient(dbhost, dbport)
    db = client.list_company
    for file_name in file_list:
        frame = pd.read_csv(file_name, encoding='gbk', skip_blank_lines=True)
        if frame.empty:
            print("No data in file ", file_name)
            continue
        frame['机构ID'] = frame['机构ID'].apply(lambda x: '{0:0>6}'.format(x))
        frame['_id'] = frame['机构ID'] + frame['报告年度']
        tframe = frame.T
        tframe.index = tframe.index.str.encode('utf-8')
        data = json.loads(tframe.to_json(force_ascii=False)).values()
        if re_table.match(file_name) is not None:
            my_collection = re_table.match(file_name).group(1)
            try:
                result = db[my_collection].insert_many(data)
                id_list.append(result.inserted_ids)
                archives_path = os.path.join(os.path.abspath('.'), 'archives', os.path.split(file_name)[1])
                os.replace(file_name, archives_path)
            except Exception as e:
                print(e.details)
                print(file_name)
                # Move error file to error folder
                error_path = os.path.join(os.path.abspath('.'), 'error file', os.path.split(file_name)[1])
                # os.rename(file_name, error_path)
                os.replace(file_name, error_path)
        else:
            print("Collection not found for files", file_name)
            return None
    return id_list


def initstocklist(dbhost="localhost", dbport=27017, collection_name="sz_stock", file_name=None, id_column="A股代码"):
    """
    
    :param dbhost: 
    :param dbport: 
    :param stock_type: sz|sh
    :param file_name: absolute file name
    :return: result_id,or None
    """
    inserted_list = []
    frame = pd.read_csv(file_name)
    if frame.empty:
        print("No data in file ", file_name)
        return None
    if collection_name == 'sz_stock':
        frame['公司代码'] = frame['公司代码'].apply(lambda x: '{0:0>6}'.format(x))
        frame_a = frame[pd.Series(frame['A股上市日期']).notnull()].copy()
        frame_b = frame[pd.Series(frame['A股上市日期']).isnull()].copy()
        frame_a["_id"] = frame_a['公司代码']
        frame_b["_id"] = frame_b['B股代码']
        frame_a['A股代码'] = frame_a['A股代码'].apply(lambda x: str(int(x)))
        frame_a['A股代码'] = frame_a['A股代码'].apply(lambda x: '{0:0>6}'.format(x))
        frame = None
        frame = frame_a.append(frame_b)
    else:
        frame[id_column] = frame[id_column].apply(lambda x: str(x))
        frame["_id"] = frame[id_column]
    tframe = frame.T
    data = json.loads(tframe.to_json(force_ascii=False)).values()
    client = MongoClient(dbhost, dbport)
    db = client.list_company
    try:
        results = db[collection_name].insert_many(data)
        inserted_list.append(results.inserted_ids)
    except Exception as e:
        print(e.details)
        return None
    return inserted_list


def exportdatatodf(conditions={}, dbhost="localhost", dbport=27017, database="", collection=""):
    """
    Export data from mongo db in dataframe with conditions
    :param conditions: 
    :param dbhost: 
    :param dbport: 
    :param database: 
    :param collection: 
    :return: DataFrame
    """
    client = MongoClient(dbhost, dbport)
    db = client[database]
    results = db[collection].find(conditions)
    frame = pd.DataFrame(list(results))
    return frame


def validate_stock(data_base=None, collection="fzb", stock_table="sh_stock"):
    # db = mongodb_utility.connect_db(db_name="list_company")
    stock_df = mongodb_utility.export2df(database=data_base, collection=stock_table)
    report_df = mongodb_utility.export2df(database=data_base, collection=collection)

    missing_stock = stock_df[~stock_df['_id'].isin(report_df['机构ID'])]
    # exclude B stock
    missing_stock_a = missing_stock[pd.Series(missing_stock['A股上市日期']).notnull()][["_id", "A股上市日期"]]
    missing_stock_a["A股上市日期"] = missing_stock_a["A股上市日期"].apply(lambda x: str(x.strip()))
    return missing_stock_a


def validate_reports_download(table1='fzb', table2='lrb', auto_download=False):
    db = mongodb_utility.connect_db(db_name="list_company")
    df1 = mongodb_utility.export2df(database=db, collection=table1)
    df2 = mongodb_utility.export2df(database=db, collection=table2)
    t1_notin_t2 = df1[~df1['_id'].isin(df2['_id'])][['_id', '机构ID', '报告年度']]
    t1_notin_t2['报告年度'] = t1_notin_t2['报告年度'].apply(lambda x: str(x.strip())[0:4])
    t1_notin_t2 = t1_notin_t2.drop_duplicates(['机构ID', '报告年度'])
    missing_t2 = t1_notin_t2[['机构ID', '报告年度']].copy()
    missing_t2['max_year'] = missing_t2['报告年度']
    download_list = missing_t2.values.tolist()
    print(len(download_list))
    if auto_download:
        url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
        frDownloader.getFR(url=url, stock_list=download_list, types=[table2])
    return download_list


def validate_bw_reports():
    db = mongodb_utility.connect_db(db_name="list_company")
    fzb_df = mongodb_utility.export2df(database=db, collection="fzb")
    llb_df = mongodb_utility.export2df(database=db, collection="llb")
    lrb_df = mongodb_utility.export2df(database=db, collection="lrb")

    missing_fzb_in_lrb = fzb_df[~fzb_df['_id'].isin(lrb_df['_id'])][['_id', '机构ID', '报告年度']]
    print(missing_fzb_in_lrb)
    missing_fzb_in_lrb.to_csv('missing_fzb_lrb.csv')

    missing_fzb_in_llb = fzb_df[~fzb_df['_id'].isin(llb_df['_id'])][['_id', '机构ID', '报告年度']]
    missing_fzb_in_llb.to_csv('missing_fzb_llb.csv')

    missing_lrb_in_fzb = lrb_df[~lrb_df['_id'].isin(fzb_df['_id'])][['_id', '机构ID', '报告年度']]
    missing_lrb_in_fzb.to_csv('missing_lrb_fzb.csv')

    missing_llb_in_fzb = llb_df[~llb_df['_id'].isin(fzb_df['_id'])][['_id', '机构ID', '报告年度']]
    missing_llb_in_fzb.to_csv('missing_llb_fzb.csv')

    missing_lrb_in_llb = lrb_df[~lrb_df['_id'].isin(llb_df['_id'])][['_id', '机构ID', '报告年度']]
    missing_lrb_in_llb.to_csv('missing_lrb_llb.csv')

    missing_llb_in_lrb = llb_df[~llb_df['_id'].isin(lrb_df['_id'])][['_id', '机构ID', '报告年度']]
    missing_llb_in_lrb.to_csv('missing_llb_lrb.csv')


def validate_data():
    db = mongodb_utility.connect_db(db_name="list_company")
    sz_df = mongodb_utility.export2df(database=db, collection="sz_stock")
    sh_df = mongodb_utility.export2df(database=db, collection="sh_stock")
    fzb_df = mongodb_utility.export2df(database=db, collection="fzb")
    # llb_df = mongodb_utility.export2df(database=db,collection="llb")
    # lrb_df = mongodb_utility.export2df(database=db,collection="lrb")

    # missing_fzb_sz = sz_df[~sz_df['_id'].isin(fzb_df['机构ID'])]
    missing_fzb_sh = sh_df[~sh_df['_id'].isin(fzb_df['机构ID'])]
    missing_sh_a = missing_fzb_sh[pd.Series(missing_fzb_sh['A股上市日期']).notnull()][["_id", "A股上市日期"]]
    # print(missing_sh_a["A股上市日期"])
    # missing_sh_a["A股上市日期"] = missing_sh_a["A股上市日期"].apply(lambda x: x.strip())
    missing_sh_a["A股上市日期"] = missing_sh_a["A股上市日期"].apply(lambda x: str(x.strip())[0:4])
    missing_sh_2017 = missing_sh_a[missing_sh_a["A股上市日期"] < "2017"].copy()
    print(missing_sh_2017.count())
    missing_sh_2017["max_year"] = "2016"
    missing_sh_2017["A股上市日期"] = "2016"
    download_list = missing_sh_2017.values.tolist()
    """download missing data
    """
    url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    # frDownloader.getFR(url=url, stock_list=download_list)


    # missing_fzb_sh.to_csv("missing_fzb_sh.csv")
    # print(missing_fzb_sh.count())
    return


def append_data_from_new():
    filter_str = r'.*(sz|sh)_(lrb|fzb|llb)_\d{6}_\d{4}\.csv'
    file_path = os.path.join(os.path.abspath('.'), 'new')
    print("file path = ", file_path)
    inserted_list = initimportdb(path=file_path, expression=filter_str)
    print(len(inserted_list))


def export_to_csv(collection="fzb"):
    column_name = collection + "_columns.csv"
    with open(column_name, mode='r', newline='', encoding='utf-8') as f:
        columns = list(csv.reader(f))
        columns = columns[0]

    df = exportdatatodf(database="list_company", collection=collection)
    # sorted_df = df.sort_values(by='_id')
    sorted_df = df.reindex_axis(columns, axis=1)
    out_file_name = collection + "_out.csv"
    sorted_df.to_csv(out_file_name, encoding="UTF-8")


if __name__ == '__main__':
    """validate data"""
    # validate_data()
    # validate_bw_reports()
    # validate_reports_download(table1="fzb",table2="llb",auto_download=True)

    # db = mongodb_utility.connect_db(db_name="list_company")
    """validate SH A stock and download missing stock    """
    """
    missing_list = validate_stock(data_base=db, collection='fzb', stock_table='sz_stock')
    missing_list["A股上市日期"] = missing_list["A股上市日期"].apply(lambda x: str(x.strip())[0:4])
    missing_2016 = missing_list[missing_list["A股上市日期"] < "2017"].copy()
    print(missing_2016.count())
    missing_2016["max_year"] = "2016"
    download_list = missing_2016.values.tolist()
    """
    """download missing data"""
    # url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
    # frDownloader.getFR(url=url, stock_list=download_list)

    """import data from csv to db"""
    # filter_str = r'.*(sz|sh)_(lrb|fzb|llb)_\d{6}_\d{4}\.csv'
    # inserted_list = initimportdb(path="./sh", expression=filter_str)
    # file_path = os.path.join(os.path.abspath('.'), 'sz')
    # file_path = os.path.join(os.path.abspath('.'), 'sh')
    """append data from ./new"""
    append_data_from_new()
    """
    filter_str = r'.*(sz|sh)_(lrb|fzb|llb)_\d{6}_\d{4}\.csv'
    file_path = os.path.join(os.path.abspath('.'), 'new')
    print("file path = ", file_path)
    inserted_list = initimportdb(path=file_path, expression=filter_str)
    print(len(inserted_list))
    """

    """Export collection to csv
    """
    # export_to_csv("fzb")
    # export_to_csv("lrb")
    # export_to_csv("llb")
    """
    with open("fzb_columns.csv",mode='r',newline='',encoding='utf-8') as f:
        fzb_columns = list(csv.reader(f))
        fzb_columns = fzb_columns[0]
        #fzb_columns.insert(0,"_id")
        #print(fzb_columns)

    df = exportdatatodf(database="list_company", collection="fzb")
    #sorted_df = df.sort_values(by='_id')
    sorted_df = df.reindex_axis(fzb_columns, axis=1)
    sorted_df.to_csv("fzb_out.csv")
    """
    """import stock code
    """
    # SZ stock insert
    # file_path = os.path.join(os.path.abspath('.'),'sz_list.csv')
    # inid = initstocklist(file_name=file_path, id_column="A股代码")
    # print(len(inid[0]))
    # Shanghai stock insert
    # file_path = os.path.join(os.path.abspath('.'),'sh_a.csv')
    # inid = initstocklist(collection_name="sh_stock", file_name=file_path, id_column="A股代码")
    # file_path = os.path.join(os.path.abspath('.'), 'sh_b.csv')
    # inid = initstocklist(collection_name="sh_stock", file_name=file_path, id_column="B股代码")
    # print(len(inid[0]))
