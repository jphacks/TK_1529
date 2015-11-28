# -*- encoding: utf-8 -*-
from xml.etree.ElementTree import *
import re

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

# main
with open("../../Downloads/jawiki-latest-pages-articles.xml") as f:
    for i in range(10000):
        title,text = page_iter(f).next()
        if title and text:
            for sent in sentence_split(text):
                print sent
                for p in list(extract_persons(title,sent)):
                    print p,
                print
