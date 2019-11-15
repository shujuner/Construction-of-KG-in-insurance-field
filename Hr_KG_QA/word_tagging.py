# encoding=utf-8

"""

@file: word_tagging.py


@desc: 定义Word类的结构；定义Tagger类，实现自然语言转为Word对象的方法。

"""
import jieba
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

        # TODO jieba不能正确切分的词语，我们人工调整其频率。
        jieba.suggest_freq(('喜剧', '电影'), True)

        jieba.suggest_freq(('生育假'), True)
        jieba.suggest_freq(('未休'), True)# 离职后未休的年假怎么办
        jieba.suggest_freq(('年休'), True)
        jieba.suggest_freq(('生育看护假'), True)
        jieba.suggest_freq(('时长'), True)

        jieba.suggest_freq(('支持序列'), True)
        jieba.suggest_freq(('技术序列1级'), True)
        jieba.suggest_freq(('技术序列2级'), True)
        jieba.suggest_freq(('技术序列3级'), True)
        jieba.suggest_freq(('技术序列4级'), True)
        jieba.suggest_freq(('技术序列5级'), True)
        jieba.suggest_freq(('专业序列1级'), True)
        jieba.suggest_freq(('专业序列2级'), True)
        jieba.suggest_freq(('专业序列3级'), True)
        jieba.suggest_freq(('专业序列4级'), True)
        jieba.suggest_freq(('专业序列5级'), True)
        jieba.suggest_freq(('管理序列M1'), True)
        jieba.suggest_freq(('管理序列M2'), True)
        jieba.suggest_freq(('管理序列M3'), True)


        jieba.suggest_freq(('部门主要负责人'), True)
        jieba.suggest_freq(('总公司部门主要负责人'), True)
        jieba.suggest_freq(('助理总经理'), True)
        jieba.suggest_freq(('总公司助理总经理'), True)
        jieba.suggest_freq(('部门副总经理'), True)
        jieba.suggest_freq(('总公司部门副总经理'), True)
        jieba.suggest_freq(('一般员工'), True)
        jieba.suggest_freq(('普通员工'), True)
        jieba.suggest_freq(('总公司一般员工'), True)
        jieba.suggest_freq(('分公司主要负责人'), True)
        jieba.suggest_freq(('分公司副总经理'), True)
        jieba.suggest_freq(('分公司助理总经理'), True)
        jieba.suggest_freq(('分公司一般员工'), True)

        jieba.suggest_freq(('怀孕未满4个月流产'), True)
        jieba.suggest_freq(('怀孕满4个月流产'), True)
        jieba.suggest_freq(('正常怀孕'), True)
        jieba.suggest_freq(('有不满1周岁婴儿'), True)






    # 同义词替换
    @staticmethod
    def tihuan_tongyici(string1):
        # tongyici_tihuan.txt是同义词表，每行是一系列同义词，用tab分割
        # 1读取同义词表：并生成一个字典。
        combine_dict = {}
        for line in open("./external_dict/tongyici_tihuan.txt", "r"):
            seperate_word = line.strip().split("\t")
            num = len(seperate_word)
            for i in range(1, num):
                combine_dict[seperate_word[i]] = seperate_word[0]

        # 2提升某些词的词频，使其能够被jieba识别出来
        jieba.suggest_freq("年假", tune=True)

        # 3将语句切分
        seg_list = jieba.cut(string1, cut_all=False)
        f = "/".join(seg_list).encode("utf-8")  # 不用utf-8编码的话，就不能和tongyici文件里的词对应上
        # print f

        # 4
        final_sentence = ""
        for word in f.split(bytes("/",'utf-8')):
            if word in combine_dict:
                word = combine_dict[word]
                final_sentence += str(word)
            else:
                final_sentence += str(word)
        # print final_sentence
        return final_sentence

    @staticmethod
    def get_word_objects(sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        return [Word(word.encode('utf-8'), tag) for word, tag in pseg.cut(sentence)]

# TODO 用于测试
if __name__ == '__main__':
    # 周星驰参加了哪些电影？
    # 我想要休产假请问需要什么材料？
    tagger = Tagger(['./external_dict/leave_title.txt', './external_dict/person_name.txt'])
    while True:
        s = input()
        s = tagger.tihuan_tongyici(s) # 同义词替换
        for i in tagger.get_word_objects(s):
            print (i.token, i.pos)
