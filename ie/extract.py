# -*- encoding: utf-8 -*-
from xml.etree.ElementTree import *
import re,gzip

# 人名の辞書
persons = {}
with open("persons.txt") as personsf:
    for line in personsf:
        persons[line.strip()] = True

# 人名かどうかを判別する関数
def is_person(tag):
    return tag.encode("utf-8") in persons

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

# 人名のリストを抽出
tag_p1 = re.compile(u"\[\[.*?\]\]")
tag_p2 = re.compile(u"\[\[.*?\|")
def extract_persons(title,sent):
    if  is_person(title):
        yield title
    for tag in tag_p1.findall(sent):
        person = tag[2:-2]
        if is_person(person):
            yield  person
    for tag in tag_p2.findall(sent):
        person = tag[2:-1]
        if is_person(person):
            yield  person

# 共演関係のパターン
pattern = re.compile(u"(共演|共著)")

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
                print title,sent
                print
                continue
                person_list = list(set(extract_persons(title,sent)))
                if len(person_list) > 1:
                    for p1 in person_list:
                        if p1 not in rel:
                            rel[p1] = []
                        temp = {"text":edit(sent,True),"title":title,"persons":[]}
                        for p2 in person_list:
                            if p2 != p1:
                                temp["persons"].append(p2)
                        rel[p1].append(temp)
                else:
                    pass
f.close()
