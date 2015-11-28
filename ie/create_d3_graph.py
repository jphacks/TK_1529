# -*- encoding: utf-8 -*-

import json

f = open("relations.json")
rel = json.load(f)
f.close()


def load_entity_data(entity):
    # アブストラクト
    try:
        jf = open("abstract/"+entity+".json")
        abst = json.load(jf)
        jf.close()
    except:
        abst = {"abst":"N/A","imageref":"N/A"}
    # 画像URL
    return abst

# 抽出結果をd3.jsで可視化するためのjsonファイルとして保存する

for target_entity in rel.keys():
    abst = load_entity_data(target_entity)
    graph = { "nodes":[{"name":target_entity,"title":target_entity,"sentence":abst["abst"],"url":"https://ja.wikipedia.org/wiki/"+target_entity,"imurl":abst["imageref"]}],
              "links" : []}

    node_num = 0
    entity2id = {target_entity:node_num}
    node_num += 1

    co_dev_infos = rel[target_entity]
    for info in co_dev_infos:
        url = "https://ja.wikipedia.org/wiki/"+info["title"]
        graph["nodes"].append({"name":"info","sentence":info["text"],"title":info["title"],"url":url})

        info_node_num = node_num
        node_num += 1

        graph["links"].append({"source":0,"target":info_node_num, "value":20})
        for entity in info["entities"]:
            if entity not in entity2id:
                abst = load_entity_data(entity)
                graph["nodes"].append({"name":entity,"title":entity,"sentence":abst["abst"],"url":"https://ja.wikipedia.org/wiki/"+entity,"imurl":abst["imageref"]})
                entity2id[entity] = node_num
                node_num += 1

            graph["links"].append({"source":info_node_num,"target":entity2id[entity], "value":20})
    j = json.dumps(graph)
    f = open("corpus/"+target_entity+".json","w")
    f.write(j)
    f.close()
