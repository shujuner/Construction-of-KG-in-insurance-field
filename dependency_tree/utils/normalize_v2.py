class Normalize():
    def __init__(self, sentence, path):
        self.sentence = sentence
        self.fields_path = path + 'fields.txt'
        self.region_path = path + 'region.txt'
        self.fields_mapping_path = path + 'fields_mapping.txt'
        self.keyword_path = path + 'keywords.txt'
        self.normalize_list = []
        self.fields_check_list = []
        self.__load_keywords()

    def __load_keywords(self):
        self.fields = []
        self.regions = []
        self.fields_mapping = []
        self.keywords = []
        with open(self.fields_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_st = line.strip()
                self.fields.append(line_st)

        with open(self.region_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_st = line.strip()
                self.regions.append(line_st)

        with open(self.fields_mapping_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_st = line.strip()
                self.fields_mapping.append(line_st)

        with open(self.keyword_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_st = line.strip()
                self.keywords.append(line_st)

        for field in self.fields:
            self.fields_check_list.append(field)

        self.fields_check_list.append('人口')

    def normalize(self):
        question_format = self.sentence.strip()
        question_format = self.replace_words(question_format)
        self.normalize_list.append(question_format)

        return self.normalize_list

    # 判断字符串是否包含在句子中
    def __check_contain(self, sentence):
        for word in self.fields_check_list:
            if word in sentence:
                return word

    def replace_words(self, question):
        question = question.replace('有多少人口', '有人口')
        question = question.replace('有多少人', '有人口')
        question = question.replace('统计', '统计有')
        question = question.replace('是', '有')

        meaningless = ['总额', '有多少呢', '有多少', '有哪些', '哪些', '多少呢', '多少', '哪个', '哪个呢',
                       '那个', '打开', '查找', '查询', '找出', '查查', '是哪一家', '是哪家', '是什么', '有什么',
                       '查看', '看看', '筛选', '选择', '选出', '筛选出', '省份有']
        # 过滤无意义词
        for word in meaningless:
            question = question.replace(word, '')

        # 字段映射
        for field in self.fields_mapping:
            field_l = field.split()
            question = question.replace(field_l[0], field_l[1])

        # 省市标准化
        for region in self.regions:
            region_l = region.split('\t')
            question = question.replace(region_l[0], region_l[1])

        # 常见字段组合
        for keyword in self.keywords:
            keyword_l = keyword.split()
            question = question.replace(keyword_l[0], keyword_l[1])

        question = question.replace('的', '有')

        if '有' not in question:
            check = self.__check_contain(question)
            if check:
                question = question.replace(check, '有' + check)

        return question


if __name__ == "__main__":
    Nl = Normalize('数学成绩不及格的学生', '../data/')
    print(Nl.normalize())
    exit()

    questions = []
    # with open('../data/question.txt', 'r', encoding='utf-8') as f:
    #     for question in f:
    #         question_st = question.strip()
    #         questions.append(question_st)
    #
    # with open('../data/test.txt', 'a+', encoding='utf-8') as f:
    #     for question in questions:
    #         norms = Normalize(question, '../data/').normalize()
    #         for norm in norms:
    #             f.write(norm + '\n')
    #             f.flush()
