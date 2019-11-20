# coding=utf-8
import os
from collections import defaultdict

# 初始化一个字典，存储每条知识对应的数据库列名

dict = defaultdict(set)


def mapping_Realition():
    d = os.path.dirname(__file__)
    parent_path = os.path.dirname(d)

    with open(parent_path + '/data/db_field_mapping/grades.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line_ = line.strip()
        dict[r'成绩'].add(line_)
    with open(parent_path + '/data/db_field_mapping/subject.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line_ = line.strip()
        dict[r'学科'].add(line_)
    dict[r'男女比例'].add(r'男女比例')
    dict[r'农村人口'].add(r'农村人口')
    dict[r'城镇人口'].add(r'城镇人口')
    dict[r'男性人口'].add(r'男性人口')
    dict[r'农村人口'].add(r'农村人口')
    dict[r'农村人口'].add(r'农村人口')
    dict[r'更新时间'].add(r'更新时间')
    dict[r'销售额'].add(r'销售额')
    dict[r'订单量'].add(r'订单量')
    dict[r'成绩'].add(r'成绩')
    dict[r'车型'].add(r'面包车')
    dict[r'车辆颜色'].add(r'银色')
    dict[r'工作时长'].add(r'工作时长')
    dict[r'班级'].add(r'121班')
    dict[r'导演'].add(r'冯小刚')
    dict[r'演员'].add(r'刘德华')
    dict[r'一级部门'].add(r'平台支持部')
    dict[r'一级部门'].add(r'技术开发部')
    dict[r'公司名'].add(r'泰山集团')
    dict[r'银行'].add(r'农行')
    dict[r'车辆颜色'].add(r'白色')
    dict[r'车辆颜色'].add(r'黑色')
    dict[r'地区'].add(r'华北')
    dict[r'电影'].add(r'一吻定情')
    dict[r'人名'].add(r'罗家')
    dict[r'电影'].add(r'流浪地球')
    dict[r'电影'].add(r'飞驰人生')

    return dict
