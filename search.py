#coding:utf-8
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser


ix = open_dir("indexdir")
with ix.searcher() as searcher:
    parser = QueryParser("title", ix.schema)
    myquery = parser.parse("中山公园")
    results = searcher.search(myquery)
    print(len(results))
    for r in results:
        print(r)