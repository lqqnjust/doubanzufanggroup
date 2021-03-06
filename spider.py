# coding:utf-8
import os
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import requests
from lxml import etree
analyzer = ChineseAnalyzer()

schema = Schema(city=TEXT(stored=True), title=TEXT(stored=True,analyzer=analyzer), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))

indexdir = 'indexdir/'
if not os.path.exists(indexdir):
    os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
else:
    ix = open_dir("indexdir")

# from elasticsearch import Elasticsearch

# es = Elasticsearch(hosts=["localhost:9200"], timeout=5000)

urls = {
    "上海":"https://www.douban.com/group/581823/discussion?start=0"
}

class Spider:
    def __init__(self,urls):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        }
        self.session = requests.Session()
        self.urls = urls
        
    def run(self):
        for city, url in self.urls.items():
            
            response = self.session.get(url, headers=self.headers)
            doc = etree.HTML(response.content)
            title_eles = doc.xpath('//td[@class="title"]')
            for title_ele in title_eles:
                title = title_ele.xpath('./a/text()')[0].strip()
                print(title)
                href = title_ele.xpath('./a/@href')[0]
                print(href)
                content = self.gettopic(href)
                writer = ix.writer()
                writer.add_document(city=city, title=title, content=content,
                    path=href)
                writer.commit()
                # id = href.split("/")[-2]
                # data = {
                #     'id':id,
                #     'title':title,
                #     'href':href,
                #     'content':content
                # }
                # es.index(index="my-index", doc_type="test-type", id=id, body=data)



    def gettopic(self, url):
        response = self.session.get(url, headers = self.headers)
        doc = etree.HTML(response.content)
        contents=doc.xpath("//div[@class='topic-richtext']/*/text()")
        str = '\n'.join(contents)
        return str
    

def main():
    spider = Spider(urls)
    spider.run()

if __name__ == '__main__':
    main()