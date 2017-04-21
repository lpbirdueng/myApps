# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import json
from Common import file_util
import re
import os
import csv



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
            except Exception as e:
                print(e.details)
                print(file_name)
                # Move error file to error folder
                error_path = os.path.join(os.path.abspath('.'), 'error file', os.path.split(file_name)[1])
                os.rename(file_name, error_path)
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
        frame['A股代码'] = frame['A股代码'].apply(lambda x: '{0:0>6}'.format(x))
        frame['公司代码'] = frame['公司代码'].apply(lambda x: '{0:0>6}'.format(x))
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


if __name__ == '__main__':
    """import data from csv to db"""
    filter_str = r'.*(sz|sh)_(lrb|fzb|llb)_\d{6}_\d{4}\.csv'
    # inserted_list = initimportdb(path="./sh", expression=filter_str)
    # file_path = os.path.join(os.path.abspath('.'), 'sz')
    # file_path = os.path.join(os.path.abspath('.'), 'sh')
    # print("file path = ", file_path)
    # inserted_list = initimportdb(path=file_path, expression=filter_str)
    # print(len(inserted_list))
    """Export collection to csv
    """
    with open("fzb_columns.csv",mode='r',newline='',encoding='utf-8') as f:
        fzb_columns = csv.reader(f)
        print(fzb_columns)
    #df = exportdatatodf(database="list_company", collection="fzb")
    #sorted_df = df.sort_values(by='_id')
    #sorted_df.to_csv("fzb_out.csv")
    """import stock code
    """
    # inid = initstocklist(file_name=".\sz_list.csv", id_column="公司代码")
    # inid = initstocklist(collection_name="sh_stock", file_name=".\sh_b.csv", id_column="B股代码")
    # print(len(inid))
