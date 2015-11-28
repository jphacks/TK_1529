# -*- encoding: utf-8 -*-
from xml.etree.ElementTree import *
import urllib2,re,json

def get_abst(title):
    query = "https://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&exsentences=3&titles="+urllib2.quote(title)
    response = urllib2.urlopen(query)
    xmlString = response.read()
    elem = fromstring(xmlString)
    extract = elem.find(".//extract")
    if extract is not None:
        return extract.text
    else:
        return False

f = open("detected_entities.txt")
i = 0
for line in f:
    if i % 100 == 0:
        print i
    i += 1
    title = line.strip()
    data = {"abst":"N/A","imageref":"N/A"}
    abst = get_abst(title)
    if abst:
        # これが概要
        data["abst"] = abst
    jf = open("abstract/"+title+".json","w")
    json.dump(data,jf)
    jf.close()
f.close()
