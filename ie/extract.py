# -*- encoding: utf-8 -*-
from xml.etree.ElementTree import *

# wikipedia のタイトルと本文を出力するイテレータ
def page_iter(f):
    page = ''
    for line in f:
        page += line.strip()+"\n"
        if line.strip() == "</page>":
            try:
                elem = fromstring(page)
                title =  elem.find(".//title").text
                text =  elem.find(".//text").text
                page = ""
            except:
                title, text = "", ""
                pass
            page = ""
            if title and text:
                yield (title, text)


with open("../../Downloads/jawiki-latest-pages-articles.xml") as f:
    for i in range(100):
        title,text = page_iter(f).next()
        if title and text:
            print title,text
