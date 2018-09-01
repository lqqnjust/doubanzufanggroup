#coding:utf-8

from flask import Flask 
from flask import render_template
from flask import request

from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser


ix = open_dir("indexdir")
searcher =  ix.searcher()
    # parser = QueryParser("title", ix.schema)
    # myquery = parser.parse("中山公园")
    # results = searcher.search(myquery)
    # print(len(results))
    # for r in results:
    #     print(r)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods = ['POST'])
def search():
    search = request.form['search']
    print(search)
    myquery = And([Term("content", search), Term("title", search)])
    results = searcher.search(myquery)
    print(len(results))
    return render_template('search.html',results=results)

if __name__ == "__main__":
    app.run(debug=True)