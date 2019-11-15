# encoding=utf-8

"""

@file: query_main.py

@desc:main函数，整合整个处理流程。

"""
import jena_sparql_endpoint
import question2sparql

if __name__ == '__main__':
    # TODO 连接Fuseki服务器。
    fuseki = jena_sparql_endpoint.JenaFuseki()
    # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
    q2s = question2sparql.Question2Sparql(['./external_dict/leave_title.txt', './external_dict/person_name.txt'])

    while True:
        question = input()

        my_query = q2s.get_sparql(question.encode('utf-8').decode('utf-8'))# 解析问题，生成sparsql
        # print my_query
        if my_query is not None:
            result = fuseki.get_sparql_result(my_query)
            value = fuseki.get_sparql_result_value(result) # 使用sparsql查询结果

            # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
            if isinstance(value, bool):
                if value is True:
                    print ('可以的。')
                else:
                    print ('不行啊。') 
            else:
                # TODO 查询结果为空，根据OWA，回答“不知道”
                if len(value) == 0:
                    print ('I don\'t know. ')
                elif len(value) == 1:
                    print (value[0])
                else:
                    output = ''
                    for v in value:
                        output += v + u'、'
                    print (output[0:-1])

        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            print ('I can\'t understand.  没有理解您的问题，请尝试规范您的用语~')

        print ('#' * 100)
# 请问年休假需要什么材料?