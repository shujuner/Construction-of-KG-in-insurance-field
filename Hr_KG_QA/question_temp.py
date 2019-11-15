# encoding=utf-8

"""
@file: question_temp.py

@desc:
设置问题模板，为每个模板设置对应的SPARQL语句。demo提供如下模板：
1. 某演员演了什么电影
2. 某电影有哪些演员出演
3. 演员A和演员B合作出演了哪些电影
4. 某演员参演的评分大于X的电影有哪些
5. 某演员出演过哪些类型的电影
6. 某演员出演的XX类型电影有哪些。
7. 某演员出演了多少部电影。
8. 某演员是喜剧演员吗。
9. 某演员的生日/出生地/英文名/简介
10. 某电影的简介/上映日期/评分

读者可以自己定义其他的匹配规则。
"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re


# 词语的 token和 pos
class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token.decode('utf-8'))
        m2 = self.pos.match(word.pos.encode('utf-8').decode('utf-8'))
        return m1 and m2

# 匹配问题类型 规则的方法
class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        return self.action(matches), self.condition_num

# 匹配具体关键词的方法
class KeywordRule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
            # print i,j,sentence[i].token,sentence[i+1].token,sentence[i+2].token
        if len(matches) == 0:
            return None
        else:
            return self.action()


# TODO SPARQL前缀和模板
SPARQL_PREXIX = u"""
prefix : <http://www.hr_kg_qa.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"



# TODO 定义自然语言的 关键词
pos_person = "nr"
pos_movie = "nz"
pos_number = "m"
pos_leave = 'nj' # 代表假期？
pos_EmployeePosition = 'nepo' #代表雇员职位
pos_EmployeeType = 'net' #代表雇员职级
pos_EmployeePregnancy = 'nepr'

person_entity = (W(pos=pos_person))
movie_entity = (W(pos=pos_movie))
number_entity = (W(pos=pos_number))
leave_entity = (W(pos=pos_leave)) # pos为nj的词语代表 请假 的实体
EmployeePosition_entity = (W(pos=pos_EmployeePosition)) # pos为nepo的词语代表雇员职位 的实体
EmployeeType_entity = (W(pos=pos_EmployeeType)) # pos为nep的词语代表雇员职位 的实体
EmployeePregnancy_entity = (W(pos=pos_EmployeePregnancy)) # pos为nepr的词语代表雇员职位 的实体


adventure = W("冒险")
fantasy = W("奇幻")
animation = (W("动画") | W("动画片"))
drama = (W("剧情") | W("剧情片"))
thriller = (W("恐怖") | W("恐怖片"))
family = W("家庭")
war = (W("战争") | W("战争片"))
TV = W("电视")
genre = (adventure | fantasy | animation | drama | thriller| family | war
         | TV)


actor = (W("演员") | W("艺人") | W("表演者"))
movie = (W("电影") | W("影片") | W("片子") | W("片") | W("剧"))
category = (W("类型") | W("种类"))
several = (W("多少") | W("几部"))

higher = (W("大于") | W("高于"))
lower = (W("小于") | W("低于"))
compare = (higher | lower)

birth = (W("生日") | W("出生") + W("日期") | W("出生"))
birth_place = (W("出生地") | W("出生"))
english_name = (W("英文名") | W("英文") + W("名字"))
introduction = (W("介绍") | W("是") + W("谁") | W("简介"))
person_basic = (birth | birth_place | english_name | introduction)

rating = (W("评分") | W("分") | W("分数"))
release = (W("上映"))
movie_basic = (rating | introduction | release)

when = (W("何时") | W("时候"))
where = (W("哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))
need = (W("需要") | W("要")| W("需不需要")| W("准备")| W("提供")) # 我写的


# 关于请假的信息：

leave_treatment = (W("待遇") | W("薪资")| W("福利")| W("奖金")| W("工资")) # 请假期间福利待遇 的关键词
leave_duration = (W("时长") | W("多久")| W("多长")| W("几天")| W("时间")| W("天")) # 请假时长 的关键词
leave_reLegalHolidays = (W("节日") | W("双休日")| W("法定假日")| W("法定")| W("法定节日") | W("法定节假日")| W("周末")| W("休息日"))# 与节假日关系 的关键词
leave_compensation = (W("赔偿") | W("补偿")| W("没休")| W("休满")| W("未休") | W("未休完")| W("休完"))# 未休赔偿 的关键词
leave_material = (W("手续") | W("材料")| W("资料")| W("凭证")| W("证件")) # 所需材料 的关键词
leave_precondition = (W("条件") | W("所需条件")| W("才能")| W("怎样能")| W("前提")| W("随时")| W("能否")| W("要求")) # 前提条件 的关键词
leave_process  = (W("流程") | W("程序")| W("过程")| W("审批")| W("批下来"))# 请假流程 的关键词
leave_canSplit = (W("拆分") |W("拆开") |W("一半")|W("一部分")| W("分开")| W("分次")| W("分割")) # 能否分开休息 的关键词

leave_togetherWith = (W("一起") | W("额外")) # 能否与其他假期一起休息 的关键词

# 别忘记 把上面的加一起
leave_basic =(leave_canSplit | leave_process | leave_precondition|leave_material|leave_compensation
              | leave_reLegalHolidays |leave_duration| leave_treatment)

# EmployeePregnancy = (W("怀孕") |W("流产") |W("产假")|W("婴儿")| W("宝宝")| W("哺乳")| W("双胞胎")| W("多胞胎")) # 怀孕状态 的关键词
# employee_type  = (W("序列") | W("M1")| W("M2")| W("M3")| W("支持序列")| W("管理序列") | W("专业序列")| # 职级序列 的关键词
#                   W("支持")| W("专业")| W("专业序列1级")| W("专业序列1级")| W("专业序列2级")| W("专业序列3级")| W("专业序列4级")|
#                   W("专业序列5级")| W("管理序列M1")| W("管理序列M1")| W("管理序列M1")| W("支持序列"))
# employee_position = (W("总公司") | W("分公司")| W("部门")| W("负责人")| W("助理")| W("管理序列")| W("管理序列")| # 职位 的关键词
#                      W("总公司部门主要负责人")| W("总公司助理总经理")| W("总公司部门副总经理")| W("总公司一般员工")
#                      | W("分公司主要负责人")| W("分公司副总经理")| W("分公司一般员工"))



# 第四步 给出 具体答案
class PropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_adventure_value():
        return u'冒险'


    @staticmethod
    def return_higher_value():
        return u'>'

    @staticmethod
    def return_lower_value():
        return u'<'

    @staticmethod
    def return_birth_value():
        return u':personBirthDay'

    @staticmethod
    def return_birth_place_value():
        return u':personBirthPlace'


#################### 关于请假的
    @staticmethod
    def return_leave_name_value():
        return u':LeaveName' # 假期名称
    @staticmethod
    def return_leave_treatment_value():
        return u':LeaveTreatment' # 假期待遇
    @staticmethod
    def return_leave_duration_value():
        return u':LeaveDuration'# 假期时长
    @staticmethod
    def return_leave_reLegalHolidays_value():
        return u':LeaveReLegalHolidays'# 假期与节假日关系
    @staticmethod
    def return_leave_compensation_value():
        return u':LeaveCompensation'# 假期未休补偿
    @staticmethod
    def return_leave_material_value():
        return u':LeaveMaterial'# 假期所需材料
    @staticmethod
    def return_leave_precondition_value():
        return u':LeavePrecondition'# 假期所需 条件
    @staticmethod
    def return_leave_process_value():
        return u':LeaveProcess'# 假期申请流程
    @staticmethod
    def return_leave_canSplit_value():
        return u':LeaveCanSplit'# 假期能否拆分
    @staticmethod
    def return_leave_togetherWith_value():
        return u':LeaveTogetherWith'# 假期能和哪个别的假期一起休息


# 第三步：根据 问题类型  找具体问题
# TODO 具体的属性词匹配规则 第三步：根据 问题类型  找具体问题
genre_keyword_rules = [
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + adventure + Star(Any(), greedy=False) + (
    movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_adventure_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + fantasy + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_fantasy_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + animation + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_animation_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + drama + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_drama_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + thriller + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_thriller_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + action + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_action_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + comedy + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_comedy_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + history + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_history_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + western + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_western_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + horror + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_horror_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + crime + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_crime_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + documentary + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_documentary_value),
    # KeywordRule(
    #     condition=person_entity + Star(Any(), greedy=False) + science_fiction + Star(Any(), greedy=False) + (
    #     movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_fiction_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + mystery + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_mystery_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + music + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_music_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + romance + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_romance_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + family + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_family_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + war + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_war_value),
    # KeywordRule(condition=person_entity + Star(Any(), greedy=False) + TV + Star(Any(), greedy=False) + (
    # movie | Star(Any(), greedy=False)), action=PropertyValueSet.return_tv_value)
]

compare_keyword_rules = [
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + higher + number_entity + Star(Any(),
                                                                                                    greedy=False) + movie + Star(
        Any(), greedy=False), action=PropertyValueSet.return_higher_value),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + lower + number_entity + Star(Any(),
                                                                                                   greedy=False) + movie + Star(
        Any(), greedy=False), action=PropertyValueSet.return_lower_value)
]

person_basic_keyword_rules = [
    KeywordRule(
        condition=(person_entity + Star(Any(), greedy=False) + where + birth_place + Star(Any(), greedy=False)) | (
        person_entity + Star(Any(), greedy=False) + birth_place + Star(Any(), greedy=False)),
        action=PropertyValueSet.return_birth_place_value),
    KeywordRule(
        condition=person_entity + Star(Disjunction(Any(), where), greedy=False) + birth + Star(Any(), greedy=False),
        action=PropertyValueSet.return_birth_value),

]

movie_basic_keyword_rules = [

]

# 关于请假 的基本属性问题：
leave_basic_keyword_rules = [
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_treatment + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_treatment_value), # 待遇
    KeywordRule(condition=leave_treatment  + Star(Any(), greedy=False) + leave_entity + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_treatment_value), # 待遇2:反序
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_duration + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_duration_value),# 时长
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_reLegalHolidays + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_reLegalHolidays_value), # 与节假日关系
    KeywordRule(condition=leave_reLegalHolidays + Star(Any(), greedy=False) + leave_entity + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_reLegalHolidays_value), # 与节假日关系2:反序
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_compensation + Star(Any(), greedy=False) ,
                action=PropertyValueSet.return_leave_compensation_value), # 未休补偿
    KeywordRule(condition = leave_compensation + Star(Any(), greedy=False) + leave_entity + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_compensation_value),  # 未休补偿2:反序
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_material + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_material_value), # 准备材料
    KeywordRule(condition= leave_material + Star(Any(), greedy=False) + leave_entity + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_material_value), # 准备材料2：反序
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_precondition + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_precondition_value), # 前提条件
    KeywordRule(condition=leave_precondition + Star(Any(), greedy=False) + leave_entity + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_precondition_value),  # 前提条件2：反序
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_process + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_process_value), # 请假流程
    KeywordRule(condition= leave_process + Star(Any(), greedy=False) +  leave_entity + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_process_value), # 请假流程2：反序
    KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_canSplit + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_canSplit_value),  # 能否分开休
    KeywordRule(condition= leave_canSplit + Star(Any(), greedy=False) + leave_entity  + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_canSplit_value),  # 能否分开休2：反序
]
# 关于请假（没有实体，使用上次的实体） 的基本属性问题：
leave_basic_keyword_without_entity_rules = [
    KeywordRule(condition=leave_treatment + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_treatment_value), # 待遇
    KeywordRule(condition=leave_duration + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_duration_value),# 时长
    KeywordRule(condition=leave_reLegalHolidays + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_reLegalHolidays_value), # 与节假日关系
    KeywordRule(condition=leave_compensation + Star(Any(), greedy=False) ,
                action=PropertyValueSet.return_leave_compensation_value), # 未休补偿
    KeywordRule(condition=leave_material + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_material_value), # 准备材料
    KeywordRule(condition=leave_precondition + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_precondition_value), # 前提条件
    KeywordRule(condition=leave_process + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_process_value), # 请假流程
    KeywordRule(condition=leave_canSplit + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_canSplit_value),  # 能否分开休
]
# 关于请假 的一起休：
leave_together_keyword_rules = [
        KeywordRule(condition=leave_entity + Star(Any(), greedy=False) + leave_togetherWith + Star(Any(), greedy=False),
                action=PropertyValueSet.return_leave_togetherWith_value), # 一起休
]

# 这是第二步 找问题类型
class QuestionSet:
    def __init__(self):
        # 定义两个变量，分别保存上次对话的实体 和 属性，用来循环对话
        # 注意：使用的时候使用QuestionSet.Placeholder1_entity这种方式
        Placeholder1_entity = None
        Placeholder2_description = None
        pass


    @staticmethod
    def has_actor_question(word_objects):
        """
        哪些演员参演了某电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_movie:
                e = u"?m :movieTitle '{movie}'." \
                    u"?m :hasActor ?a." \
                    u"?a :personName ?x".format(movie=w.token.decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break

        return sparql


    @staticmethod
    def has_cooperation_question(word_objects):
        """
        演员A和演员B有哪些合作的电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        person1 = None
        person2 = None

        for w in word_objects:
            if w.pos == pos_person:
                if person1 is None:
                    person1 = w.token
                else:
                    person2 = w.token
        if person1 is not None and person2 is not None:
            e = u"?p1 :personName '{person1}'." \
                u"?p2 :personName '{person2}'." \
                u"?p1 :hasActedIn ?m." \
                u"?p2 :hasActedIn ?m." \
                u"?m :movieTitle ?x".format(person1=person1.decode('utf-8'), person2=person2.decode('utf-8'))

            return SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                          select=select,
                                          expression=e)
        else:
            return None


    @staticmethod
    def has_compare_question(word_objects):
        """
        某演员参演的评分高于X的电影有哪些？
        :param word_objects:
        :return:
        """
        select = u"?x"

        person = None
        number = None
        keyword = None

        for r in compare_keyword_rules:
            keyword = r.apply(word_objects)
            if keyword is not None:
                break

        for w in word_objects:
            if w.pos == pos_person:
                person = w.token

            if w.pos == pos_number:
                number = w.token

        if person is not None and number is not None:

            e = u"?p :personName '{person}'." \
                u"?p :hasActedIn ?m." \
                u"?m :movieTitle ?x." \
                u"?m :movieRating ?r." \
                u"filter(?r {mark} {number})".format(person=person.decode('utf-8'), number=number.decode('utf-8'),
                                                     mark=keyword)

            return SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                            select=select,
                                            expression=e)
        else:
            return None

    @staticmethod
    def has_movie_type_question(word_objects):
        """
        某演员演了哪些类型的电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :personName '{person}'." \
                    u"?s :hasActedIn ?m." \
                    u"?m :hasGenre ?g." \
                    u"?g :genreName ?x".format(person=w.token.decode('utf-8'))

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_specific_type_movie_question(word_objects):
        """
        某演员演了什么类型（指定类型，喜剧、恐怖等）的电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        keyword = None
        for r in genre_keyword_rules:
            keyword = r.apply(word_objects)

            if keyword is not None:
                break

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :personName '{person}'." \
                    u"?s :hasActedIn ?m." \
                    u"?m :hasGenre ?g." \
                    u"?g :genreName '{keyword}'." \
                    u"?m :movieTitle ?x".format(person=w.token.decode('utf-8'), keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def has_quantity_question(word_objects):
        """
        某演员演了多少部电影
        :param word_objects:
        :return:
        """
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :personName '{person}'." \
                    u"?s :hasActedIn ?x.".format(person=w.token.decode('utf-8'))

                sparql = SPARQL_COUNT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break

        return sparql

    @staticmethod
    def is_comedian_question(word_objects):
        """
        某演员是喜剧演员吗
        :param word_objects:
        :return:
        """
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :personName '{person}'." \
                    u"?s rdf:type :Comedian.".format(person=w.token.decode('utf-8'))

                sparql = SPARQL_ASK_TEM.format(prefix=SPARQL_PREXIX, expression=e)
                break

        return sparql

    @staticmethod
    def has_basic_person_info_question(word_objects):
        """
        某演员的基本信息是什么
        :param word_objects:
        :return:
        """

        keyword = None
        for r in person_basic_keyword_rules:
            keyword = r.apply(word_objects)
            if keyword is not None:
                break

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e = u"?s :personName '{person}'." \
                    u"?s {keyword} ?x.".format(person=w.token.decode('utf-8'), keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)

                break

        return sparql

    @staticmethod
    def has_basic_movie_info_question(word_objects):
        """
        某电影的基本信息是什么
        :param word_objects:
        :return:
        """

        keyword = None
        for r in leave_basic_keyword_rules:
            keyword = r.apply(word_objects)
            if keyword is not None:
                break

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_movie:
                e = u"?s :movieTitle '{movie}'." \
                    u"?s {keyword} ?x.".format(movie=w.token.decode('utf-8'), keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)

                break

        return sparql

    ######## 查询请假的一些基本信息
    @staticmethod
    def has_basic_leave_info_question(word_objects):
        """
        查询请假的一些基本信息
        :param word_objects:
        :return:
        """
        keyword = None
        for r in leave_basic_keyword_rules: # 去假期详细信息 具体问题中查询，
            keyword = r.apply(word_objects) # 调用关键字匹配方式 查询
            if keyword is not None: # 查到关键字 就 转化为sparsql
                break
        # print '-----leave基本信息关键词：',keyword  # 打印问句关键词
        # 增加一个判断，如果到这一步keyword 还是= None；就说明， 找到了问题类型，但是没有关键词，不能继续查询：
        if keyword == None:
            return None # 直接返回，不要查询了 否则会报错
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_leave:
                e = u"?s :LeaveName '{Leave}'." \
                    u"?s {keyword} ?x.".format(Leave=w.token.decode('utf-8'), keyword=keyword)

                QuestionSet.Placeholder1_entity = w.token.decode('utf-8') # 记录本次问句的 实习和描述 方面下次问句使用
                QuestionSet.Placeholder2_description = keyword
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break

        #  如果问的是假期申请流程，给用户提示输入职位；并将占位符修改为EmployeePositionLeaveProcess
        if keyword == u':LeaveProcess':
            QuestionSet.Placeholder2_description = u':EmployeePositionLeaveProcess'

        # 如果本次问的是年休假的时长，给用户提示输入职级序列；EmployeeTypeAnnualLeaveDuration
        if QuestionSet.Placeholder1_entity == u'年休假' and keyword ==u':LeaveDuration':
            QuestionSet.Placeholder2_description = u':EmployeeTypeAnnualLeaveDuration'
        # 如果问的是 产假的时长， 则提示用户输入怀孕状态。
        if QuestionSet.Placeholder1_entity == u'产假' and keyword ==u':LeaveDuration':
            QuestionSet.Placeholder2_description = u':EmployeePregnancyLeaveDuration'

        return sparql




    @staticmethod
    def has_leave_together_info_question(word_objects):
        """
        查询某假期可以和什么假期一起休
        :param word_objects:
        :return:
        """
        keyword = None
        for r in leave_together_keyword_rules:  # 去假期详细信息 具体问题中查询，
            keyword = r.apply(word_objects)  # 调用关键字匹配方式 查询
            if keyword is not None:  # 查到关键字 就 转化为sparsql
                break
        # print '-----leave一起休关键词：', keyword  # 打印问句关键词
        # 增加一个判断，如果到这一步keyword 还是= None；就说明， 找到了问题类型，但是没有关键词，不能继续查询：
        if keyword == None:
            return None  # 直接返回，不要查询了 否则会报错
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_leave:
                e = u"?s :LeaveName '{Leave}'." \
                    u"?s {keyword} ?o."\
                    u"?o :LeaveName ?x".format(Leave=w.token.decode('utf-8'), keyword=keyword)

                QuestionSet.Placeholder1_entity = w.token.decode('utf-8')  # 记录本次问句的 实习和描述 方面下次问句使用
                QuestionSet.Placeholder2_description = keyword
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break
        return sparql
    @staticmethod
    def Prompt_user_has_leave_attributes(word_objects):
        """
        用户只写了假期名字
        给用户该 假期的概念，并提醒用户输入想问的属性
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_leave:

                e = u"?s :LeaveName '{Leave}'." \
                    u"?s {keyword} ?x.".format(Leave=w.token.decode('utf-8'), keyword=u':LeaveConception')
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                QuestionSet.Placeholder1_entity = w.token.decode('utf-8')  # 记录本次问句的 实习 方面下次问句使用
                break
        return sparql
    @staticmethod
    def has_basic_leave_info_question_without_entity(word_objects):
        """
        用户只给了属性，
       使用个上次问题的实体，匹配本次的 属性
        :param word_objects:
        :return:
        """
        keyword = None
        for r in leave_basic_keyword_without_entity_rules: # 去假期详细信息 具体问题中查询，
            keyword = r.apply(word_objects) # 调用关键字匹配方式 查询
            if keyword is not None: # 查到关键字 就 转化为sparsql
                break
        # print '-----leave基本信息关键词_without_entity：',keyword  # 打印问句关键词
        # 增加一个判断，如果到这一步keyword 还是= None；就说明， 找到了问题类型，但是没有关键词，不能继续查询：
        if keyword == None:
            return None # 直接返回，不要查询了 否则会报错
        select = u"?x"
        sparql = None

        e = u"?s :LeaveName '{Leave}'." \
            u"?s {keyword} ?x.".format(Leave=QuestionSet.Placeholder1_entity, keyword=keyword)

        QuestionSet.Placeholder2_description = keyword# 记录本次问句的 描述 方面下次问句使用
        sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)

        #  如果问的是假期申请流程，给用户提示输入职位；并将占位符修改为EmployeePositionLeaveProcess
        if keyword ==u':LeaveProcess':
            QuestionSet.Placeholder2_description = u':EmployeePositionLeaveProcess'
        # 如果本次问的是年休假的时长，给用户提示输入职级序列；EmployeeTypeAnnualLeaveDuration
        if QuestionSet.Placeholder1_entity == u'年休假' and keyword ==u':LeaveDuration':
            QuestionSet.Placeholder2_description = u':EmployeeTypeAnnualLeaveDuration'
        if QuestionSet.Placeholder1_entity == u'产假' and keyword ==u':LeaveDuration':
            QuestionSet.Placeholder2_description = u':EmployeePregnancyLeaveDuration'
        return sparql

    @staticmethod
    def has_EmployeePositionLeaveProcess(word_objects):
        """
        用户只给了职位，
       使用个上次问题的 Placeholder2_description，即请假流程
        :param word_objects:
        :return:
        """
        # print '-----EmployeePositionLeaveProcess查询'

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_EmployeePosition:
                QuestionSet.Placeholder1_entity = w.token.decode('utf-8')# 使用类变量记录这次问的问题是关于哪个 职位的
                e = u"?s :EmployeePositionName '{EmployeePositionName}'." \
                    u"?s {keyword} ?x.".format(EmployeePositionName=w.token.decode('utf-8'), keyword=QuestionSet.Placeholder2_description)
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break
        return sparql

    @staticmethod
    def has_EmployeeTypeAnnualLeaveDuration(word_objects):
        """
        用户只给了职级，
       使用个上次问题设定的 Placeholder2_description，即 has_EmployeeTypeAnnualLeaveDuration 不同职级对应的年假时长
        :param word_objects:
        :return:
        """
        # print '-----has_EmployeeTypeAnnualLeaveDuration'

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_EmployeeType:

                e = u"?s :EmployeeTypeName '{EmployeeTypeName}'." \
                    u"?s {keyword} ?x.".format(EmployeeTypeName=w.token.decode('utf-8'), keyword=QuestionSet.Placeholder2_description)
                QuestionSet.Placeholder1_entity = w.token.decode('utf-8')  # 使用类变量记录这次问的问题是关于哪个 职级的
                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break
        return sparql

    @staticmethod
    def has_EmployeePregnancyLeaveDuration(word_objects):
        """
        用户只给了怀孕状态，
       使用个上次问题设定的 Placeholder2_description，即 has_EmployeePregnancyLeaveDuration 不同状态对应的产假时长
        :param word_objects:
        :return:
        """
        # print '-----has_EmployeePregnancyLeaveDuration'
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_EmployeePregnancy:
                e = u"?s :EmployeePregnancyName '{EmployeePregnancyName}'." \
                    u"?s {keyword} ?x.".format(EmployeePregnancyName=w.token.decode('utf-8'),
                                               keyword=QuestionSet.Placeholder2_description)
                QuestionSet.Placeholder1_entity = w.token.decode('utf-8')  # 使用类变量记录这次问的问题是关于哪个 状态的

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREXIX, select=select, expression=e)
                break
        return sparql

# 第一步：给出问题模版，用refo正则匹配。
# TODO 问题模板/匹配规则  这是 第一步！
"""

1. 某假期的各种基本属性
2. 某假期可以和什么假期一起休息？
"""
rules = [
    Rule(condition_num=2, condition=person_entity + Star(Any(), greedy=False) + movie + Star(Any(), greedy=False), action=QuestionSet.has_actor_question),
    Rule(condition_num=2, condition=(movie_entity + Star(Any(), greedy=False) + actor + Star(Any(), greedy=False)) | (actor + Star(Any(), greedy=False) + movie_entity + Star(Any(), greedy=False)), action=QuestionSet.has_actor_question),
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + person_entity + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=QuestionSet.has_cooperation_question),
    Rule(condition_num=4, condition=person_entity + Star(Any(), greedy=False) + compare + number_entity + Star(Any(), greedy=False) + movie + Star(Any(), greedy=False), action=QuestionSet.has_compare_question),
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + category + Star(Any(), greedy=False) + movie, action=QuestionSet.has_movie_type_question),
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + genre + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=QuestionSet.has_specific_type_movie_question),
    Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + several + Star(Any(), greedy=False) + (movie | Star(Any(), greedy=False)), action=QuestionSet.has_quantity_question),
    # Rule(condition_num=3, condition=person_entity + Star(Any(), greedy=False) + comedy + actor + Star(Any(), greedy=False), action=QuestionSet.is_comedian_question),
    Rule(condition_num=3, condition=(person_entity + Star(Any(), greedy=False) + (when | where) + person_basic + Star(Any(), greedy=False)) | (person_entity + Star(Any(), greedy=False) + person_basic + Star(Any(), greedy=False)), action=QuestionSet.has_basic_person_info_question),
    Rule(condition_num=2, condition=movie_entity + Star(Any(), greedy=False) + movie_basic + Star(Any(), greedy=False), action=QuestionSet.has_basic_movie_info_question),

    ######假期的
    ## 1. 查询假期 基本属性
    Rule(condition_num=2, condition=(leave_entity + Star(Any(), greedy=False) + leave_basic + Star(Any(), greedy=False))|(leave_basic  + Star(Any(), greedy=False) + leave_entity + Star(Any(), greedy=False)), action=QuestionSet.has_basic_leave_info_question),
    ## 2. 查询假期 可以一起休
    Rule(condition_num=2, condition=(leave_entity + Star(Any(), greedy=False) + leave_togetherWith + Star(Any(), greedy=False)), action=QuestionSet.has_leave_together_info_question),
    ## 3.查询年休假天数
    # condition_num=1说明为起始问题：只说 哪个 假期
    Rule(condition_num=1, condition=(leave_entity + Star(Any(), greedy=False) ), action=QuestionSet.Prompt_user_has_leave_attributes),
    # 只说 属性，使用上次问题的实体Placeholder1_entity
    Rule(condition_num=1, condition=(leave_basic + Star(Any(), greedy=False) ), action=QuestionSet.has_basic_leave_info_question_without_entity),
    ##只说 职位，说明是查询 请假流程
    Rule(condition_num=1, condition=(EmployeePosition_entity + Star(Any(), greedy=False) ), action=QuestionSet.has_EmployeePositionLeaveProcess),
    ##只说 职级序列，说明是查询 年假时长
    Rule(condition_num=1, condition=(EmployeeType_entity + Star(Any(), greedy=False) ), action=QuestionSet.has_EmployeeTypeAnnualLeaveDuration),
    ##只说 怀孕状态，说明是查询 不同产假时长
    Rule(condition_num=1, condition=(EmployeePregnancy_entity + Star(Any(), greedy=False)),action=QuestionSet.has_EmployeePregnancyLeaveDuration),

]
