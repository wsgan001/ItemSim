#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fasttext
from annoy import AnnoyIndex
import random
import jieba

class ItemSim(object):

    def __init__(self):
        pass

    def Fname(self, fileL):
        basedir = "corpus/"  # 这是我的文件地址，需跟据文件夹位置进行更改
        listi = [str(i) for i in range(10, fileL+11)]
        file_list = []
        for e in listi:
            filename = basedir + e
            file_list.append(filename)

        return file_list

    def Cut(self, fileL):
        file_list = self.Fname(fileL)
        for file in file_list:
            filename_in = file + '.txt'
            with open(filename_in, 'r') as fr:
                text = fr.read()
            seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
            outline = ' '.join(seg_text)
            outline = outline.encode("utf-8") + "\n"
            filename_out = file + '_cut.txt'
            fout = open(filename_out, 'w+')
            fout.write(outline)
            fout.close()

    def Keyword(self, fileL):
        import jieba.analyse as analyse
        file_list = self.Fname(fileL)
        for file in file_list:
            filename_in = file + '.txt'
            filename_out = file + '_keywords.txt'
            fout = open(filename_out, 'w+')
            with open(filename_in, 'r') as fr:
                text = fr.read()

            for key in analyse.extract_tags(text, 50, withWeight=False):
                # 使用jieba.analyse.extract_tags()参数提取关键字,默认参数为50
                word = key.encode('utf-8')
                fout.write(word + '\n')

    def PreProcess(self, fileL):
        import jieba

        ##生成fastext的训练集

        fout = open("news_fasttext_train.txt", "w+")

        file_list = self.Fname(fileL)
        for file in file_list:
            filename_in = file + '.txt'
            with open(filename_in, 'r') as fr:
                text = fr.read()
            seg_text = jieba.cut(text.replace("\t", " ").replace("\n", " "))
            outline = ' '.join(seg_text)
            outline = outline.encode("utf-8") + "\n"
            fout.write(outline)

        fout.close()

    def Item2vec(self, fileL):
        file_list = self.Fname(fileL)

        # 根据切词结果训练模型
        filename_cut = 'news_fasttext_train.txt'
        model = fasttext.skipgram(filename_cut, 'model')

        fout = open('item2vec.txt', 'w+')
        i = 9
        for file in file_list:
            i += 1
            #叠加关键词的向量
            vec = []
            filename_key = file + '_keywords.txt'
            fin = open(filename_key, 'r')
            while True:
                line = fin.readline()
                if line:
                    keyword = line.strip()
                    # print keyword
                    k_vec = model[keyword]
                    # print k_vec
                    if len(vec) == 0:
                        vec = k_vec
                    else:
                        vec = list(map(lambda x: x[0] + x[1], zip(vec, k_vec)))
                else:
                    break
            fin.close()

            fout.write(str(vec) + '\n')

        fout.close()

    def FindSim(self, fileL):

        f = 100

        t = AnnoyIndex(f)  # Length of item vector that will be indexed

        #读取向量
        fin = open('item2vec.txt', 'r')
        i = 0
        while True:
            line = fin.readline()
            if line:
                v = eval(line.strip())
                t.add_item(i, v)
                i += 1
            else:
                break
        fin.close()

        t.build(10)  # 10 trees
        t.save('test.ann')

        u = AnnoyIndex(f)
        u.load('test.ann')  # super fast, will just mmap the file
        print(u.get_nns_by_item(0, 3))  # will find the 1000 nearest neighbors

def main():
    itemsim = ItemSim()
    # itemsim.Keyword(10)
    # itemsim.PreProcess(10)
    # itemsim.Item2vec(10)
    itemsim.FindSim(10)

if __name__ == '__main__':
    main()