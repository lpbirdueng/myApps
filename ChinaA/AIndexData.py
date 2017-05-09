# -*- coding: utf-8 -*-
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
print(sys.path)

from Common.downloader import Downloader
from datetime import timedelta
from datetime import date


def getIndexData(url_prefix, days=-1, start_date=date.today(), path=None, max_errors=20):
    D = Downloader()
    single_day = timedelta(days=1)
    # current_date = date.today() - single_day
    current_date = start_date - single_day
    if days > 0:
        for day in range(days):
            if current_date.weekday() >= 5:
                current_date = current_date - single_day
                continue
            date_str = str(current_date.strftime('%Y%m%d'))
            url = url_prefix + date_str + '.zip'
            if path is None:
                fullfilename = date_str + '.zip'
            else:
                fullfilename = path + "\\" + date_str + '.zip'
            D.saveZipToLocal(url, filename=fullfilename, extract=True)
            current_date = current_date - single_day
    else:
        num_errors = 0
        while True:
            if current_date.weekday() >= 5:
                current_date = current_date - single_day
                continue
            date_str = str(current_date.strftime('%Y%m%d'))
            url = url_prefix + date_str + '.zip'
            if path is None:
                fullfilename = date_str + '.zip'
            else:
                fullfilename = path + "\\" + date_str + '.zip'
            if D.saveZipToLocal(url, filename=fullfilename, extract=True):
                num_errors = 0
            else:
                num_errors = num_errors + 1
            if num_errors >= max_errors:
                break
            current_date = current_date - single_day


if __name__ == '__main__':
    getIndexData(url_prefix="http://115.29.204.48/syl/", days=3)
    getIndexData(url_prefix="http://115.29.204.48/syl/csi", days=3)
    getIndexData(url_prefix="http://115.29.204.48/syl/bk", days=3)
    # start_date = date(2016,8,9)
    # getIndexData(url_prefix="http://115.29.204.48/syl/",start_date = start_date)
    # getIndexData(url_prefix="http://115.29.204.48/syl/csi")
    # getIndexData(url_prefix="http://115.29.204.48/syl/bk",start_date = start_date)
