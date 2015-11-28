# -*- encoding: utf-8 -*-
from xml.etree.ElementTree import *
import re,gzip

# 人名の辞書
entities = {}
with open("entities.txt") as entitiesf:
    for line in entitiesf:
        entities[line.strip()] = True

# 人名かどうかを判別する関数
def is_entity(tag):
    return tag.encode("utf-8") in entities

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

# 文に分割する関数
def sentence_split(text):
    return text.split(u"。")

# 組織のリストを抽出
tag_p1 = re.compile(u"\[\[.*?\]\]")
tag_p2 = re.compile(u"\[\[.*?\|")
def extract_entities(title,sent):
    if  is_entity(title):
        yield title
    for tag in tag_p1.findall(sent):
        entity = tag[2:-2]
        if is_entity(entity):
            yield  entity
    for tag in tag_p2.findall(sent):
        entiry = tag[2:-1]
        if is_entity(entity):
            yield  entity

# 共同開発関係のパターン
pattern = re.compile(u"(共同|協働|協同|合同|共に)で?.?(開発|運営|製造|実施|生産|製造|研究|制作|発表)")

# 文を整形する関数
def edit(txt,is_info=False):
    p1 = re.compile(u"(\[\[)([^\]]+?)(\|)([^\]]+?)(\]\])")
    p2 = re.compile(u"(\[\[)([^\]]+?)(\]\])")
    p3 = re.compile(u"{{[L|l]ang-en-short\|(.+?)}}")
    p4 = re.compile(u"'''(.+?)'''")
    p5 = re.compile(u"''(.+?)''")
    p6 = re.compile(u"{{\s?[Cc]ite .+}}")
    p7 = re.compile(u"{{NASDAQ\|(.+?)}}")
    p8 = re.compile(u"\[http:.+?\]")
    p9 = re.compile(u"{{\s?refnest.+}}")
    p10 = re.compile(u"\*")
    left = u"<span id='entity'>"
    right = u"</span>"
    txt =  p1.sub(lambda a: left + a.group(4) + right if a.group(2).encode("utf-8") in entities and is_info  else a.group(4),txt)
    txt = p2.sub(lambda a: left + a.group(2) + right if a.group(2).encode("utf-8") in entities and is_info else a.group(2),txt)
    txt = p3.sub(lambda a: a.group(1),txt)
    txt = p4.sub(lambda a: "<span id='strong'>"+a.group(1)+"</span>",txt)
    txt = p5.sub(lambda a: a.group(1),txt)
    txt = p6.sub("",txt)
    txt = p7.sub(lambda a: a.group(1),txt)
    txt = p8.sub("",txt)
    txt = p9.sub("",txt)
    co_dev_left = u"<span id = 'relation'>"
    co_dev_right = u"</span>"
    txt = pattern.sub(lambda a:co_dev_left+a.group(0)+co_dev_right if is_info else a.group(0),txt)
    txt = p10.sub("",txt)
    return txt


rel = {}
f = gzip.open("../../Downloads/jawiki-latest-pages-articles.xml.gz")
j = 1
for i in range(1000000):
    if i % 10000 == 0:
        print i
    title,text = page_iter(f).next()
    for para in text.split("\n"):
        for sent in sentence_split(para):
            result = pattern.search(sent)
            if result:
                entity_list = list(set(extract_entities(title,sent)))
                if len(entity_list) > 1:
                    for p1 in entity_list:
                        if p1 not in rel:
                            rel[p1] = []
                        temp = {"text":edit(sent,True),"title":title,"entities":[]}
                        for p2 in entity_list:
                            if p2 != p1:
                                temp["entities"].append(p2)
                        rel[p1].append(temp)
                else:
                    pass
f.close()

import json
j = json.dumps(rel)
f = open("relations.json","w")
f.write(j)
f.close()

f = open("detected_entities.txt","w")
for k in rel.keys():
    f.write(k.encode("utf-8")+"\n")
f.close()
