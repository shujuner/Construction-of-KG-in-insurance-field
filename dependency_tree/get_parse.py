import re

from utils import Mapping_DB
from utils.hanlp_util import HaNLPUtil
from utils.normalize_v3 import Normalize
from utils.preprocess import Preprocess


class parse(object):
    def __init__(self):
        self.subject = {}
        self.predicate = {}
        self.object = {}

    # 初始化分词、词性、依存语法树
    def __init_attributes(self, sentence):
        HaUtil = HaNLPUtil(sentence)
        self.words = HaUtil.get_words()
        self.postags = HaUtil.get_postags()
        parsers = HaUtil.get_dependency_parser()
        self.parsers = parsers.getWordArray()

    def run(self, sentence):
        self.__init_attributes(sentence)

        for idx, parser in enumerate(self.parsers):
            print(parser)


if __name__ == '__main__':
    line_sp = "中国人寿保险股份有限公司是中国最大的人寿保险公司,纽约、香港、上海三地上市的" \
              "中国人寿保险向个人及团体提供人寿保险、意外保险和健康保险产品"
    print(line_sp)
    parse().run(line_sp)
