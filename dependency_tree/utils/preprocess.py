from utils.common import *


class Preprocess(object):
    def __init__(self, sentence):
        self.sentence = sentence
        self.sentence = self.__preprocess_sentence()
        self.question_class = []

    def __preprocess_sentence(self):
        # 把"各类型""各类别"改为"各类"：
        num = 0
        for i, word in enumerate(self.sentence):
            if word == "各" and self.sentence[i+1] == "类" and self.sentence[i+2] in ["型", "别"]:
                num = i + 2
                break
        sen = ''
        if num != 0:
            for i, word in enumerate(self.sentence):
                if i != num:
                    sen += word
            print(sen)
            return sen
        # 把"比。。。多"改为"大于"：
        w1 = -1
        w2 = -1
        for i_1, word_1 in enumerate(self.sentence):
            if word_1 == "比":
                w1 = i_1
            if word_1 == "多":
                w2 = i_1
                break
        if w1 != -1 and w2 != -1:
            for i_2, word_2 in enumerate(self.sentence):
                if i_2 == w1:
                    sen += "大于"
                    continue
                if i_2 == w2:
                    sen += ""
                    continue
                sen += word_2
            print(sen)
            return sen
        print(self.sentence)
        return self.sentence

    # 对问题进行分类
    def classifier(self):
        sum_str_list = ['多少', '人口']
        avg_str_list = ['平均']  # 一元
        max_str_list = ['最多', '最大', '最高', '最快', '最好', '最晚', '最长', '最贵']  # 一元
        min_str_list = ['最少', '最小', '最低', '最慢', '最坏', '最差', '最早', '最短', '最便宜']  # 一元
        group_str_list = ['按', '统计', '分组']  # 一元
        compare_str_list = ['比', '超过', '大于', '小于', '少于', '不多于', '不少于', '多于',
                            '高于', '低于', '不超过', '不大于', '不小于', '不高于', '不低于',
                            '大于等于', '小于等于', '去除', '不足', '最贵', '最高', '最恶毒', '不是']  # 二元
        proportion_str_list = ['占比']  # 二元
        trend_str_list = ['趋势']  # 一元
        list_str_list = ['各个', '各', '不同', '每天', '每个', '每月', '每年', '每', '排序', '有省', '省份', '有区',
                         '有区名', '有城市', '有员工', '有年份', '有企业', '有电影', '有公司', '有十人', '有十个', '有学生',
                         '个学生', '有天气', "有车辆信息", "有数据", "前十", "分布", "有车", "有颜色", "有帖子"]  # 一元
        count_str_list = ['几个']
        if check_contain(self.sentence, count_str_list):
            self.question_class.append('count')
        if check_contain(self.sentence, avg_str_list):
            self.question_class.append('avg')
        if check_contain(self.sentence, max_str_list):
            self.question_class.append('max')
        if check_contain(self.sentence, min_str_list):
            self.question_class.append('min')
        if check_contain(self.sentence, proportion_str_list):
            self.question_class.append('proportion')
        if check_contain(self.sentence, compare_str_list):
            if 'proportion' not in self.question_class:
                self.question_class.append('compare')
        if check_contain(self.sentence, trend_str_list):
            self.question_class.append('trend')
        if check_contain(self.sentence, list_str_list):
            self.question_class.append('list')
        if check_contain(self.sentence, group_str_list):
            self.question_class.append('group')
        if len(self.question_class) == 0:
            self.question_class.append('sum')
        if len(self.question_class) == 1 and check_contain(self.sentence, sum_str_list):
            self.question_class.append('sum')
        return self.question_class
