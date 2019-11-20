import re

class Normaize():
    def __init__(self, question):
        self.question = question
    def find_company(self):
        rule_1 = r'(.*)(名|班级)有(.*)的(.*)'
        partten = re.compile(rule_1)
        res = re.search(partten, self.question)
        print(1)
        if res:
            print(res.group())
        else:
            print('不成功')

if __name__ == "__main__":

    a = Normaize('公司名有泰山集团的平均涨跌?')
    a.find_company()



