# bert-chinese-ner

使用预训练语言模型BERT做中文命名实体识别

代码参考

- **[BERT-NER](https://github.com/kyzhouhzau/BERT-NER)**
- **[bert-chinese-ner](https://github.com/ProHiryu/bert-chinese-ner)**
- [KBQA-BERT](https://github.com/WenRichard/KBQA-BERT)
- [BERT-TF](https://github.com/google-research/bert)

## 训练
BERT_NER.py

## 结果

经过4749个epoch跑出来的结果

```
eval_f = 0.9632253
eval_precision = 0.96335554
eval_recall = 0.9632042
global_step = 4749
loss = 14.731425
```
## 测试
test_ner.py

需要加入保险相关的实体进行训练，才能更好地识别相关实体

效果如下：
```
input the test sentence:
张先生，广告公司管理人员，年薪人民币20万元。张太太，公务员，年薪6万元。女儿6岁。张先生一家到目前没有商业保险的保障，并且对保险的意识淡漠。你作为人寿保险公司的寿险顾问，运用你的专业知识解决以下问题。
[['B-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-PER', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]
PER: 张, 张, 张
识别的实体有：张张张
Time used: 0 sec
```