# -*- coding: utf-8 -*-
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


if __name__ == '__main__':
    app.run()
