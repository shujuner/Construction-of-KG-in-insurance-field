import re

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
        # print(question_format)
        question_format = self.compare_question(question_format)
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
                       '那个', '打开', '查找', '查询', '找出', '查查', '是哪一家', '是哪家', '有哪家', '是什么', '有什么',
                       '查看', '看看', '筛选', '选择', '选出', '筛选出',]
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

    '''1986年有哪些城市男人比女人少   ->  1986年男人少于女人有城市'''
    # 替换回混淆的词
    def compare_normal(self, question):
        # 混淆词表
        confuse = ['比例', '占比', '同比增长率', '环比增长值', '百分比', '多少']
        punctuation = ['?', '？', '!', '！', '.', '。']
        
        # 替换
        i = 0
        for i, word in zip(range(len(confuse)), confuse):
            question = question.replace(word, '替换词'+str(i))
        # 去除标点
        for p in punctuation:
            question = question.replace(p, '')
        
        return question
    
    # 将混淆的词换回来
    def compare_denormal(self, question):
        confuse = ['比例', '占比', '同比增长率', '环比增长值', '百分比', '多少']
        repl_rule = r'(替换词)+[0-9]*'
        
        replace_word = re.search(repl_rule, question)
        while replace_word:
            word_num = replace_word.group().replace('替换词', '')
            word_num = int(word_num)
            question = question.replace(replace_word.group(), confuse[word_num])
            replace_word = re.search(repl_rule, question)
        return question
    
    # 比较问题标准化
    def compare_question_normalize(self, question):
        normalize_rule = r'(有)*(哪些|哪个|哪几|哪几个|哪一个|哪场|哪只|哪家|哪|多少|几个)(城市|省份|省|年份|年|区|电影|股票|公司)*(的)*'
        key_rule = r'(城市|省份|省|年|区)'
        normalize_word = re.search(normalize_rule, question)
        if normalize_word:
            key = re.search(key_rule, normalize_word.group())
            question = question.replace(normalize_word.group(), '')
            if key:
                question += '有' + key.group()
        
        return question
    
    # 处理比较类问题
    def compare_question(self, question):
        # 先判断问题是否包含比较，需要先过滤掉 比例 占比 同比增长率 环比增长值 等混淆的词
        norm_question = self.compare_normal(question)

        # 比较问题转换
        m_compare_1 = re.search(r'(.*)(比|没有)+(.*)', norm_question)
        if m_compare_1:
            question_list = self.deal_compare_question(norm_question)
            question_list = self.compare_denormal(question_list)
            question_list = self.compare_question_normalize(question_list)
            return question_list
        
        return question

    # 包含比较，转化为 '比较词1 多|少|... 比较词2' 的格式
    def deal_compare_question(self, question):
        # 规范化比较词
        dict_normalize = {'多': ['多于', '少于'], '少':['少于', '多于'], 
                          '大': ['大于', '小于'], '小':['小于', '大于'],
                          '高': ['高于', '低于'], '低':['低于', '高于'],
                          '强': ['强于', '弱于'], '弱':['弱于', '强于']}
        
        # 规范化规则
        cmp_rule1 = r'(比)+(.+)(多|少|大|小|高|低|强|弱)+((?!(的|有)).)*(的|有)+'
        cmp_rule2 = r'(比)+(.+)(多|少|大|小|高|低|强|弱)+(.*)'
        cmp_rule3 = r'(没有)+(.+)(多|少|大|小|高|低|强|弱)+((?!(的|有)).)*(的|有)+'
        cmp_rule4 = r'(没有)+(.+)(多|少|大|小|高|低|强|弱)+(.*)'
        # 判断规范比较词是否已存在
        nomarlized = r'(多于|少于|大于|小于|高于|低于|强于|弱于)'
        
        # 提取比较关键词
        cmp_key1 = r'(多|少|大|小|高|低)+(.*)'
        
        compare = re.search(cmp_rule1, question)
        # rule1满足
        if compare:
            # 去除 的|有
            key_cmp = re.search(cmp_key1, compare.group()).group()[:-1]
            # 规范化
            question = question.replace(key_cmp, '')
            question = question.replace('比', key_cmp)
            
            # 比较词不规范，需要规范化
            nomarlized_word = re.search(nomarlized, key_cmp)
            if (nomarlized_word == None):
                question = question.replace(key_cmp[0], dict_normalize[key_cmp[0]][0])
        else:
            compare = re.search(cmp_rule2, question)
            # rule2 满足
            if compare:
                key_cmp = re.search(cmp_key1, compare.group()).group()
                question = question.replace(key_cmp, '')
                question = question.replace('比', key_cmp)
                nomarlized_word = re.search(nomarlized, key_cmp)
                if (nomarlized_word == None):
                    question = question.replace(key_cmp[0], dict_normalize[key_cmp[0]][0])
            else:
                # rule3 满足
                compare = re.search(cmp_rule3, question)
                if compare:
                    key_cmp = re.search(cmp_key1, compare.group()).group()[:-1]
                    
                    nomarlized_word = re.search(nomarlized, key_cmp)
                    if (nomarlized_word == None):
                        question = question.replace(key_cmp, '')
                        question = question.replace('没有', key_cmp)
                        question = question.replace(key_cmp[0], dict_normalize[key_cmp[0]][1])
                    else:
                        question = question.replace(key_cmp, '')
                        question = question.replace('没有', key_cmp)
                        question = question.replace(key_cmp[0:2], dict_normalize[key_cmp[0]][1])
                else:
                    compare = re.search(cmp_rule4, question)
                    # rule4 满足
                    if compare:
                        key_cmp = re.search(cmp_key1, compare.group()).group()
                        
                        nomarlized_word = re.search(nomarlized, key_cmp)
                        if (nomarlized_word == None):
                            question = question.replace(key_cmp, '')
                            question = question.replace('没有', key_cmp)
                            question = question.replace(key_cmp[0], dict_normalize[key_cmp[0]][1])
                        else:
                            question = question.replace(key_cmp, '')
                            question = question.replace('没有', key_cmp)
                            question = question.replace(key_cmp[0:2], dict_normalize[key_cmp[0]][1])
        return question

if __name__ == "__main__":
    Nl = Normalize('股价最高的公司是哪家', '../data/')
    print(Nl.normalize())

    questions = []
    # with open('../data/extend_questions.txt', 'r', encoding='utf-8') as f:
    #     for question in f:
    #         question_st = question.strip()
    #         questions.append(question_st)
    #
    # with open('../output/extend_questions_normalize.txt', 'a+', encoding='utf-8') as f:
    #     for question in questions:
    #         norms = Normalize(question, '../data/').normalize()
    #         for norm in norms:
    #             f.write(norm + '\n')
    #             f.flush()
