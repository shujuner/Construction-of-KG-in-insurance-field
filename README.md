### 2019.11.13-2019.11.16
#### Relation Classification via Convolutional Deep Neural Network
> 这一篇是关系抽取中一个比较经典的模型, 就是一个CNN, 甚至这个框架可以直接拿来做文本分类。输入的特征是句子特征和位置特征的拼接, 分类器就是用的一个CNN模型。

![enter description here](./images/cnn-RE.png)

> paper: [Relation Classification via Convolutional Deep Neural Network](https://www.aclweb.org/anthology/C14-1220/)

#### DeepDive
> DeepDive (http://deepdive.stanford.edu/) 是斯坦福大学开发的信息抽取系统，能处理文本、表格、图表、图片等多种格式的无结构数据，从中抽取结构化的信息。系统集成了文件分析、信息提取、信息整合、概率预测等功能。Deepdive的主要应用是特定领域的信息抽取，系统构建至今，已在交通、考古、地理、医疗等多个领域的项目实践中取得了良好的效果。DeepDive系统的基本输入包括：
> 1. 无结构数据，如自然语言文本
> 2. 现有知识库或知识图谱中的相关知识
> 3. 若干启发式规则

> DeepDive系统的基本输出包括：
> 1. 规定形式的结构化知识，可以为关系（实体1，实体2）或者属性（实体，属性值）等形式
> 2. 对每一条提取信息的概率预测

> DeepDive系统运行过程中还包括一个重要的迭代环节，即每轮输出生成后，用户需要对运行结果进行错误分析，通过特征调整、更新知识库信息、修改规则等手段干预系统的学习，这样的交互与迭代计算能使得系统的输出不断得到改进。