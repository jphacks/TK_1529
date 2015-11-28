import json
j = json.dumps(rel)
f = open("relations.json","w")
f.write(j)
f.close()


def load_person_data(person):
    # アブストラクト                                                                                                                                                                                                                                  
    try:
        jf = open("abstract/"+person+".json")
        abst = json.load(jf)
        jf.close()
    except:
        abst = {"abst":"N/A","imageref":"N/A"}
    # 画像URL                                                                                                                                                                                                                                         
    return abst

# 抽出結果をd3.jsで可視化するためのjsonファイルとして保存する                                                                                                                                                                                         
import json
for target_person in rel.keys():
    abst = load_org_data(o)
    graph = { "nodes":[{"name":target_person,"title":target_person,"sentence":abst["abst"],"url":"https://ja.wikipedia.org/wiki/"+target_person,"imurl":abst["imageref"]}],
              "links" : []}

    node_num = 0
    person2id = {o:node_num}
    node_num += 1

    co_dev_infos = rel[o]
    for info in co_dev_infos:
        url = "https://ja.wikipedia.org/wiki/"+info["title"]
        graph["nodes"].append({"name":"info","sentence":info["text"],"title":info["title"],"url":url})

        info_node_num = node_num
        node_num += 1

        graph["links"].append({"source":0,"target":info_node_num, "value":20})
        for person in info["persons"]:
            if person not in person2id:
                abst = load_person_data(person)
                graph["nodes"].append({"name":person,"title":person,"sentence":abst["abst"],"url":"https://ja.wikipedia.org/wiki/"+person,"imurl":abst["imageref"]})
                person2id[person] = node_num
                node_num += 1

            graph["links"].append({"source":info_node_num,"target":person2id[person], "value":20})
    j = json.dumps(graph)
    f = open("test_corpus/"+target_person+".json","w")
    f.write(j)
    f.close()
