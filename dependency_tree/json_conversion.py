from TripleIE.ie_v2 import TripleIE
from TripleIE.utils.normalize_v3 import Normalize
from TripleIE.utils.Mapping_DB import *

'''
    # 这个是Mapping_DB文件中的dict 用来把读入的数据所属的字段名加入到全局的dict中
    
    # 传入的值
    # data 
    
    # 输入的用户问题
    # data["text"]

    # 输入第i个的涉及到的表中的字段名称 该数据只有一个
    # data["tableInfo"]["fields"][i]["alias"]

    # 设计到的表中的样例数据 该数据存在数组中，不一定唯一
    # for str_list in data["tableInfo"]["fields"][0]["data"]:
    #     print(str_list)

'''


def json_AddToDict(data):
    # 先把每个表的字段对应的样例数据加进去
    for i in range(len(data["tableInfo"]["fields"])):
        if "data" in data["tableInfo"]["fields"][i]:
            for aliasList in data["tableInfo"]["fields"][i]["data"]:
                dict[data["tableInfo"]["fields"][i]["name"]].add(aliasList)
        if "dataEnum" in data["tableInfo"]["fields"][i]:
            for dataEnumList in data["tableInfo"]["fields"][i]["dataEnum"]:
                dict[data["tableInfo"]["fields"][i]["name"]].add(dataEnumList)
    if data["knowledges"][0]["name"]:
        for str_knowledge in data["knowledges"][0]["fields"]:
            dict[data["knowledges"][0]["name"]].add(str_knowledge)




if __name__ == "__main__":
    data = {
        "text": "云南的人口数量",
        "knowledges": [{
            "id": "1",
            "name": "一线城市",
            "fields": ["城市"]
        }],
        "tableInfo": {
            "name": "data",
            "dbName": "None",
            "fields": [{
                "name": "省份",
                "dbFieldType": "NAME",
                "type": "TEXT",
                "alias": "省份",
                "dbFieldName": "file_f_137060cd9c92dc3d",
                "dataEnum": ["四川", "辽宁", "福建", "广东", "贵州", "黑龙江", "海南", "浙江", "安徽", "内蒙古", "山东", "云南", "西藏", "甘肃", "江西",
                             "江苏", "广西", "河北", "山西", "新疆", "湖北", "陕西", "青海", "宁夏", "吉林", "湖南", "河南", "上海", "北京"],
                "data": ["四川", "四川", "四川", "四川", "四川", "四川", "四川", "四川", "四川", "四川"],
                "desc": "None",
                "id": "field_725d4ec0293999847",
                "distinctCount": 29
            }, {
                "name": "城市",
                "dbFieldType": "NAME",
                "type": "TEXT",
                "alias": "城市",
                "dbFieldName": "file_f_35b363b9c0fdcd61",
                "dataEnum": ["成都", "大连", "福州", "广州", "贵阳", "哈尔滨", "海口", "杭州", "合肥", "呼和浩特", "济南", "昆明", "拉萨", "兰州",
                             "南昌", "南京", "南宁", "宁波", "青岛", "厦门", "沈阳", "石家庄", "太原", "乌鲁木齐", "武汉", "西安", "西宁", "银川",
                             "长春", "长沙", "郑州", "浦东", "海淀", "东城"],
                "data": ["成都", "成都", "成都", "成都", "成都", "成都", "成都", "成都", "成都", "成都"],
                "desc": "None",
                "id": "field_8d6b687cd83974072",
                "distinctCount": 34
            }, {
                "name": "男性人口（万人）",
                "dbFieldType": "NAME",
                "alias": "男性人口（万人）",
                "type": "NUM",
                "dbFieldName": "file_f_2967bf6c57ee386e7",
                "desc": "None",
                "id": "field_f6ceaa00bb8f90044",
                "distinctCount": 558
            }, {
                "name": "女性人口（万人）",
                "dbFieldType": "NAME",
                "alias": "女性人口（万人）",
                "type": "NUM",
                "dbFieldName": "file_f_56dde7e25da22ae50",
                "desc": "None",
                "id": "field_b08103e81c4d66bab",
                "distinctCount": 557
            }, {
                "name": "城镇人口（万人）",
                "dbFieldType": "NAME",
                "alias": "城镇人口（万人）",
                "type": "NUM",
                "dbFieldName": "file_f_636870b0884cbccd0",
                "desc": "None",
                "id": "field_98a67c0238059d5a9",
                "distinctCount": 528
            }, {
                "name": "农村人口（万人）",
                "dbFieldType": "NAME",
                "alias": "农村人口（万人）",
                "type": "NUM",
                "dbFieldName": "file_f_162ad6a464610f3ae",
                "desc": "None",
                "id": "field_4a04218c2f55b9a8f",
                "distinctCount": 567
            }, {
                "name": "人口(万人)",
                "dbFieldType": "NAME",
                "alias": "人口(万人)",
                "type": "NUM",
                "dbFieldName": "file_f_acfb26edf44b71da3",
                "desc": "None",
                "id": "field_3be775f04f6829e35",
                "distinctCount": 598
            }, {
                "name": "男女比例",
                "dbFieldType": "NAME",
                "alias": "男女比例",
                "type": "NUM",
                "dbFieldName": "file_f_810457c8432ca35ba",
                "desc": "None",
                "id": "field_cdf9da1a3750ee9df",
                "distinctCount": 3
            }, {
                "name": "日期",
                "dbFieldType": "NAME",
                "alias": "日期",
                "type": "DATE",
                "dbFieldName": "file_f_b7a0435ceb1326fd8",
                "desc": "None",
                "id": "field_af653d66c61e13ae8",
                "distinctCount": 25
            }],
            "dataSourceId": "ds_inner_ds",
            "desc": "",
            "dbTableName": "file_t_5e226ca0463824c92",
            "id": "table_7ed5f028a08eb9a33",
            "tableType": "NAME"
        }
    }

    json_AddToDict(data)
    Nl = Normalize(data["text"], 'data/')  # 二月平台支持部工作时长小于7小时有员工
    question = Nl.normalize()[0]
    print(question)
    IE = TripleIE()
    L = IE.run(question)
    print(L)
    '''
    public int majorityElement(int[] nums) {
       int count = 0;
        int value = 0;
        for(int i : nums){
            if(count == 0){
                value = i;
                count = 1;
            }else{
                if(i == value){
                    count++;
                }
                else{
                    count--;
                }
            }
            
        }
        return value;
    }'''
