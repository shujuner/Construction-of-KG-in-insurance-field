def format(x):
    return x.strip()


# 判断字符串是否包含在句子中
def check_contain(sentence, check_str_list):
    return any(word in sentence for word in check_str_list)
