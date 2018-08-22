#coding:utf-8
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser


ix = open_dir("indexdir")
with ix.searcher() as searcher:
    parser = QueryParser("content", ix.schema)
    myquery = parser.parse("地铁")
    results = searcher.search(myquery)
    print(len(results))
    for r in results:
        print(r)