import requests

with open('question.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line_sp = line.strip()
        print(line_sp)
        requests.post('http://kbqa.w6688j.com/get_triples',
                      json={"q": line_sp},
                      headers={"Content-Type": "application/json;charset=utf-8"})
