# -*- coding: utf-8 -*-
from sinastorage.bucket import SCSBucket
import sinastorage
from zipfile import ZipFile
from io import BytesIO


with ZipFile('test.zip', 'r') as zf:
    sinastorage.setDefaultAppInfo('16wn9n74cnZJFjffXU3K', '50706013e9a806c252aafb03ad2a3b51174e36ad')
    s = SCSBucket('saepcs', secure=False)  # secure=True 采用https访问方式
    scsResponse = s.putFile('stock/test.zip', 'test.zip')