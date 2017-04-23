# -*- coding: utf-8 -*-
from Common import mongodb_utility

con = mongodb_utility.connect_db(db_name="list_company")
results = mongodb_utility.export2df(database=con,collection="sz_stock")
print(results)