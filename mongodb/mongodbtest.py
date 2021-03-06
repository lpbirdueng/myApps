# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pymongo
from pandas import Series, DataFrame
import pandas as pd
import csv
import json
from bson.objectid import ObjectId

df = pd.read_csv("https://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENO=1&ENCODE=1&TABKEY=tab1")
print(df)
exit()
# df = pd.read_csv('sz_lrb_000001_2000.csv',encoding='gbk', converters={'机构ID': lambda x:str(x)})
# df = pd.read_table('sz_lrb_000001_1992.csv', encoding='gbk', sep=',')
df = pd.read_csv('sz_lrb_000001_2014.csv', encoding='gbk')
df['机构ID'] = df['机构ID'].apply(lambda x: '{0:0>6}'.format(x))
df['_id'] = df['机构ID'] + df['报告年度']
client = MongoClient("localhost", 27017)
db = client.test_database
for i in df.index:
    cursor = db.lrb.find_one({"_id": df.ix[i, '_id']})
    if cursor is not None:
        df = df.drop(i)
print(df)
if df.empty:
    exit()
# print(df['机构ID'])
tdf = df.T
tdf.index = tdf.index.str.encode('utf-8')
# print(tdf.columns)

data = json.loads(tdf.to_json(force_ascii=False)).values()

# print('tdf = ',tdf)
# print('tdf0 = ', tdf[0])
# data = tdf[0].to_json(force_ascii=False)
# data = json.loads(tdf.to_json(force_ascii=False))
# encoded_data = data.decode('gbk').encode('utf-8')
#print("data =", data)

# df.to_csv('out.csv',encoding='utf-8')
# data = pd.read_csv('out.csv')
"""
list = []
with open('sz_lrb_000001_2000.csv',mode='r',newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        #row = row.decode('gbk').encode('utf-8')
        #print('row = ', row)
        list.append(row)

frame = DataFrame(list[1:],columns=list[0])
#print('frame = ', frame)
"""

try:
    result = db.lrb.insert_many(data)
    print("result = ", result)
except Exception as e:
    print(e.details)
# result = db.lrb.insert_one(data)
"""insert dataformat into mongodb
for c in tdf.columns:
    data = data = json.loads(tdf[c].to_json(force_ascii=False))
    result = db.lrb.insert_one(data)
    print('result = ', result)
"""
# result = db.lrb.delete_many({"_id": '0000012014-12-31'})
# print("result = ", result.deleted_count)
cursor = db.lrb.find()
for doc in cursor:
    print(doc)
