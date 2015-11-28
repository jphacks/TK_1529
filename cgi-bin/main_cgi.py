#! /Users/simaokasonse/anaconda/bin/python2.7
# -*- coding: utf-8 -*-
import cgi
import cgitb; cgitb.enable()
import json

print "Content-type: text/javascript; charset=utf-8"
print

jf = open("redirect.json")
redirect_dict = json.load(jf)
jf.close()

form = cgi.FieldStorage()

foo = form.getfirst("query", "")

# 名寄せ
if foo.decode("utf-8") in redirect_dict:
    foo = redirect_dict[foo.decode("utf-8")]

f=open("./ie/corpus/"+foo+".json")
data = json.loads(f.read())
print json.dumps(data)
