# -*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame


def csv_to_html(file_name=None):
    df = pd.read_csv(file_name, encoding='utf-16')
    html_str = df.to_html()
    print("df =", df)
    print("html str = ", html_str)
    return html_str

if __name__ == '__main__':
    html_str = csv_to_html(file_name="hsi_11May17.csv")
    with open('test.html', mode='w') as f:
        f.write(html_str)