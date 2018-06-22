#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator

def Sim_item_count(filein, fileout, topnum):
    fin = open(filein, 'r')
    topic_list = {}
    item_list = {}
    items_keys = {}
    for j in range(2000):
        topic_list[j] = []
    while True:
        line = fin.readline()
        if line:
            if 'None' not in line:
                id, vec = line.split('&&&')
                vec = eval(vec)
                if len(vec) == 0:
                    continue
                id, item_key = id.split(':', 1)
                id = int(id)
                items_keys[id] = item_key

                item_tops = [] #初始化每个item的主题列表
                for i in range(len(vec)):
                    v = vec[i]
                    tnum = int(v[0])
                    if i <= topnum:
                        topic_list[tnum].append(id)
                        item_tops.append(tnum)
                    else:
                        break
                item_list[id] = item_tops
        else:
            break
    fin.close()
    print 'topic_list and item_list生成结束'

    # 找到每个item的相似item数
    x = []
    a = []
    for id in item_list.keys():
        x.append(id)
        item_tops = item_list[id]
        sim_items = [] #初始化每个item的相似item的列表
        for tnum in item_tops:
            topic_item_list = topic_list[tnum]
            sim_items += topic_item_list
        sim_items = set(sim_items) - set([id])
        a.append(len(sim_items))

    print '找相似item结束'

    # 写入csv文件
    import pandas as pd
    dataframe = pd.DataFrame({'top10_overlap_count': a, 'item_id': x})
    dataframe.to_csv(fileout)

def item_sim(filein, fileout1):
    # 计算item的相似度，列出最相似的topk个
    fin = open(filein, 'r')
    items_vec = {}
    items_keys = {}
    while True:
        line = fin.readline()
        if line:
            if 'None' not in line:
                id, tvec = line.split('&&&')
                id, keys = id.split(':', 1)
                id = int(id)
                items_keys[id] = keys
                tvec = eval(tvec)
                if len(tvec) == 0:
                    continue
                item_vec = [0.0]*2000 # 初始化每个item向量
                for i in range(len(tvec)):
                    v = tvec[i]
                    tnum = int(v[0])
                    tsim = float(v[1])
                    item_vec[tnum] = tsim
                items_vec[id] = item_vec
        else:
            break
    fin.close()
    print 'item向量生成结束'


    # 计算相似度并输出最相似的topk个item的id
    from annoy import AnnoyIndex

    f = 2000
    t = AnnoyIndex(f)  # Length of item vector that will be indexed
    for id in items_vec.keys():
        t.add_item(id, items_vec[id])

    t.build(10)  # 10 trees

    df1 = {}
    for id in items_vec.keys():
        p_items = [items_keys[id]]
        p_list = t.get_nns_by_item(id, 6)
        for pi in range(1, 6):
            pl = p_list[pi]
            p_items.append(str(pl) + ':' + items_keys[pl])
        df1[id] = p_items

    print '找相似item结束'

    # 写入csv文件
    import pandas as pd
    df = pd.DataFrame(df1)
    df = df.T
    df.to_csv(fileout1, sep=',', header=True, index=True)

def Intersection(filein, fileout, topnum):
    fin = open(filein, 'r')
    items_vec = {}
    items_keys = {}
    while True:
        line = fin.readline()
        if line:
            if 'None' not in line:
                id, tvec = line.split('&&&')
                id, item_key = id.split(':', 1)
                id = int(id)
                items_keys[id] = item_key
                tvec = eval(tvec)
                if len(tvec) == 0:
                    continue
                item_topic_list = [0] * 2000  # 初始化每个item的topic列表
                for i in range(len(tvec)):
                    v = tvec[i]
                    tnum = int(v[0])
                    if i <= topnum:
                        item_topic_list[tnum] = 1
                    else:
                        break
                items_vec[id] = item_topic_list
            else:
                break
    fin.close()
    print 'item生成结束'

    # 计算相似度并输出最相似的topk个item的id
    from annoy import AnnoyIndex

    f = 2000
    t = AnnoyIndex(f)  # Length of item vector that will be indexed
    for id in items_vec.keys():
        t.add_item(id, items_vec[id])

    t.build(10)  # 10 trees

    df1 = {}
    for id in items_vec.keys():
        p_items = [items_keys[id]]
        p_list = t.get_nns_by_item(id, 6)
        for pi in range(1, 6):
            pl = p_list[pi]
            p_items.append(str(pl) + ':' + items_keys[pl])
        df1[id] = p_items

    print '找相似item结束'

    # 写入csv文件
    import pandas as pd
    df = pd.DataFrame(df1)
    df = df.T
    df.to_csv(fileout, sep=',', header=True, index=True)

def Topic_count(filein, fileout):
    #记录每条数据的topic数
    fin = open(filein, 'r')
    df = {}
    while True:
        line = fin.readline()
        if line:
            if 'None' not in line:
                id, tvec = line.split('&&&')
                id, item_key = id.split(':', 1)
                id = int(id)
                tvec = eval(tvec)
                if len(tvec) > 0:
                    df[id] = [len(tvec)]

        else:
            break
    fin.close()


    # 写入csv文件
    import pandas as pd
    df = pd.DataFrame(df)
    df = df.T
    df.to_csv(fileout, sep=',', header=True, index=True)


def main():

    # #lda 新闻
    # Sim_item_count('news_lda_vec.txt', 'news_lda_item_count.csv', 10)
    #
    # item_sim('news_lda_vec.txt', 'news_lda_items_annoy.csv')
    #
    # Intersection('news_lda_vec.txt', 'news_lda_intersection.csv', 10)
    #
    Topic_count('news_lda_vec.txt', 'news_lda_topic_count.csv')
    #
    #
    # #slda 新闻
    #
    # Sim_item_count('news_slda_vec.txt', 'news_slda_item_count.csv', 10)
    #
    # item_sim('news_slda_vec.txt', 'news_slda_items_annoy.csv')
    #
    # Intersection('news_slda_vec.txt', 'news_slda_intersection.csv', 10)

    Topic_count('news_slda_vec.txt', 'news_slda_topic_count.csv')
    #
    #
    # # slda 微博
    #
    # Sim_item_count('weibo_slda_vec.txt', 'weibo_slda_item_count.csv', 10)
    #
    # item_sim('weibo_slda_vec.txt', 'weibo_slda_items_annoy.csv')
    #
    # Intersection('weibo_slda_vec.txt', 'weibo_slda_intersection.csv', 10)

    Topic_count('weibo_slda_vec.txt', 'weibo_slda_topic_count.csv')




if __name__ == '__main__':
    main()