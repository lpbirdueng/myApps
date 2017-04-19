# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import json
from Common import file_util
import re


def initimportdb(path, expression, dbhost="localhost", dbport=27017):
    file_list = file_util.get_file_list_with_filter(path=path, expression=expression)
    if file_list is None:
        return None
    re_lrb = re.compile(".*_lrb_.*")
    re_fzb = re.compile(".*_fzb_.*")
    re_llb = re.compile(".*_llb_.*")
    client = MongoClient(dbhost, dbport)
    db = client.list_company
    for file_name in file_list:
        frame = pd.read_csv(file_name, encoding='gbk')
        #print('file name = ',file_name)
        if file_name == './sh/.DS_Store':
            continue
        #print("frame = ",frame)
        frame['机构ID'] = frame['机构ID'].apply(lambda x: '{0:0>6}'.format(x))
        tframe = frame.T
        tframe.index = tframe.index.str.encode('utf-8')
        data = json.loads(tframe.to_json(force_ascii=False)).values()
        if re_fzb.match(file_name) is not None:
            result = db.fzb.insert_many(data)
            continue
        if re_lrb.match(file_name) is not None:
            result = db.lrb.insert_many(data)
            continue
        if re_llb.match(file_name) is not None:
            result = db.llb.insert_many(data)
            continue
    return


def exportdatatocsv(conditions={}, dbhost="localhost", dbport=27017, database="", collection=""):
    client = MongoClient(dbhost, dbport)
    db = client[database]
    results = db[collection].find(conditions)
    return results


if __name__ == '__main__':
    filter_str = r'.*sh_lrb|fzb|llb_\d{6}_\d{4}\.csv'
    initimportdb(path="./sh", expression=filter_str)
    #results = exportdatatocsv(database="list_company",collection="lrb")
    #frame = pd.DataFrame(list(results))
    #print(frame.ix[0])

