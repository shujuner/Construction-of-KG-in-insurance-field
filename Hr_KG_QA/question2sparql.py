# encoding=utf-8

"""
@file: question2sparql.py


@desc: 将自然语言转为SPARQL查询语句

"""
from __future__ import print_function
import question_temp
import word_tagging

class Question2Sparql:
    def __init__(self, dict_paths):

        self.tw = word_tagging.Tagger(dict_paths) # 分词 并获取词语的词性
        self.rules = question_temp.rules # 获取question_temp中的 所有类型的问题

    def get_sparql(self, question):
        """
        进行语义解析，找到匹配的模板，返回对应的SPARQL查询语句
        :param question:
        :return:
        """
        question = self.tw.tihuan_tongyici(question)# 同义词替换
        # print ('----消歧：',question)
        word_objects = self.tw.get_word_objects(question) # 返回分词后的 词组和 词性，其中 假期定义为nj类型
        # 此时word_objects包含了这句话中的所有词组。

        # print('-----问句分词：',end=' ')
        # for i in word_objects:
        #     print(i.token, i.pos ,end=' ')
        # print()

        queries_dict = dict()

        for rule in self.rules: # 第一步 寻找合适的 类型的问题
            query, num = rule.apply(word_objects)


            if query is not None:
                queries_dict[num] = query

        if len(queries_dict) == 0:
            return None
        elif len(queries_dict) == 1:
            return queries_dict.values()[0]
        else:
            # TODO 匹配多个语句，以匹配关键词最多的句子作为返回结果
            sorted_dict = sorted(queries_dict.iteritems(), key=lambda item: item[0], reverse=True)
            return sorted_dict[0][1]
