from TripleIE.utils.hanlp_util import HaNLPUtil


class TripleIE(object):
    def __init__(self, sentence):
        self.sentence = sentence
        self.subject = {}
        self.object = {}
        self.triples = []

        self.init_attributes()

    # 初始化分词、词性、依存语法树
    def init_attributes(self):
        HaUtil = HaNLPUtil(self.sentence)
        self.words = HaUtil.get_words()
        self.postags = HaUtil.get_postags()
        parsers = HaUtil.get_dependency_parser()
        self.parsers = parsers.getWordArray()
        self.sub_dicts = self.__build_sub_dicts()

        # print(parsers)
        # print(self.sub_dicts)

    # 运行主函数
    def run(self):
        # 抽取主谓宾关系
        self.extract_SBV()
        # 抽取时间关系
        self.extract_Time()
        # 抽取地点关系
        self.extract_Place()
        # 抽取定中关系
        self.extract_ATT()
        # 抽取状中关系
        self.extract_ADV()

        return self.triples

    # 抽取主谓宾关系
    def extract_SBV(self):
        for idx, parser in enumerate(self.parsers):
            if parser.CPOSTAG in 'v':
                sub_dict = self.sub_dicts[idx]

                # 存在主谓关系，取出主语
                if 'SBV' in sub_dict:
                    self.subject = {
                        'id': sub_dict['SBV'][0],
                        'val': self.words[sub_dict['SBV'][0]]
                    }

                # 存在动宾关系，取出宾语
                if 'VOB' in sub_dict:
                    self.object = {
                        'id': sub_dict['VOB'][0],
                        'val': self.words[sub_dict['VOB'][0]]
                    }

                if 'val' in self.object.keys():
                    self.triples.append("(%s, %s, ?)" % (self.object['val'], self.words[idx]))
                    if 'val' in self.subject.keys():
                        self.triples.append("(%s, %s, %s)" % (self.subject['val'], self.words[idx], self.object['val']))

    # 抽取时间关系
    def extract_Time(self):
        for idx, parser in enumerate(self.parsers):
            if parser.CPOSTAG == 'nt' and 'val' in self.object.keys():
                self.triples.append("(%s, _, %s)" % (self.words[idx], self.object['val']))

    # 抽取地点关系
    def extract_Place(self):
        for idx, parser in enumerate(self.parsers):
            # 词性为地点且不为主语的
            if parser.CPOSTAG == 'ns' \
                    and parser.DEPREL != 'SBV' \
                    and 'val' in self.object.keys():
                self.triples.append("(%s, _, %s)" % (self.words[idx], self.object['val']))

    # 抽取定中关系
    def extract_ATT(self):
        for idx, parser in enumerate(self.parsers):
            # 存在定中关系, 取出定语, 并排除已经抽取的时间关系、地点关系
            sub_dict = self.sub_dicts[idx]
            if 'ATT' in sub_dict \
                    and self.parsers[sub_dict['ATT'][0]].CPOSTAG not in ['nt', 'ns']:
                attribute_idx = sub_dict['ATT'][0]
                if 'val' in self.object.keys():
                    self.triples.append("(%s, _, %s)" % (self.words[attribute_idx], self.object['val']))

    # 抽取状中关系
    def extract_ADV(self):
        for idx, parser in enumerate(self.parsers):
            # 存在状中关系, 取出状语, 并排除已经抽取的时间关系
            sub_dict = self.sub_dicts[idx]
            if 'ADV' in sub_dict \
                    and self.parsers[sub_dict['ADV'][0]].CPOSTAG not in ['nt', 'ns'] \
                    and 'val' in self.object.keys():
                attribute_idx = sub_dict['ADV'][0]
                self.triples.append("(%s, _, %s)" % (self.words[attribute_idx], self.object['val']))

    """
    :decription: 为句子中的每个词语维护一个保存句法依存儿子节点的字典
    :args:
        words: 分词列表
        postags: 词性列表
        arcs: 句法依存列表
    """

    def __build_sub_dicts(self):
        sub_dicts = []
        for idx in range(len(self.words)):
            sub_dict = dict()
            for arc_idx, arc in enumerate(self.parsers):
                if arc.HEAD.ID == idx + 1:
                    if arc.DEPREL in sub_dict:
                        sub_dict[arc.DEPREL].append(arc_idx)
                    else:
                        sub_dict[arc.DEPREL] = []
                        sub_dict[arc.DEPREL].append(arc_idx)
            sub_dicts.append(sub_dict)

        return sub_dicts


if __name__ == "__main__":
    # with open('data/normalize.txt', 'r', encoding='utf-8') as f:
    #     questions = f.readlines()
    #
    # with open('output/normalize_out.txt', 'a+', encoding='utf-8') as f:
    #     for line in questions:
    #         line_sp = line.strip()
    #         triple_list = TripleIE(line_sp).run()
    #         f.write(line_sp + '\n')
    #         for triple in triple_list:
    #             f.write('\t' + triple + '\n')
    #         f.flush()

    IE = TripleIE('1984年全国的人口')
    print(IE.run())
