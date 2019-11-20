fields = []
with open('fields.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line_st = line.strip()
        fields.append(line_st)

suffixs = ['的全部的数量', '的全部数量', '的所有的数量', '的所有数量', '的总共的数量', '的总的数量', '的总数量',
           '的总数', '的总量', '的值', '的数量', '的数', '的量', '全部的数量', '全部数量',
           '所有的数量', '所有数量', '总共的数量', '总的数量', '总数量', '总数', '总量', '值', '数量', '数', '量']

prefixs = ['全部的', '所有的', '总共的', '总的', '全部', '所有', '总共', '总']


def generate_suffix(field):
    list = []
    for suffix in suffixs:
        list.append(field + suffix + ' ' + field)

    return list


def generate_prefix(field):
    list = []
    for prefix in prefixs:
        list.append(prefix + field + ' ' + field)

    return list


keywords = []
for field in fields:
    suffix_list = generate_suffix(field)
    prefix_list = generate_prefix(field)
    keywords += suffix_list + prefix_list

with open('keywords.txt', 'a+', encoding='utf-8') as f:
    for keyword in keywords:
        f.write(keyword + '\n')
        f.flush()
