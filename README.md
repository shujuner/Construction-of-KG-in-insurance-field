                       

## ***知识融合***

1.	基本问题：怎样将来自多个来源的关于同一个实体或概念的描述信息融合起来
2.	主要挑战：  
  -  数据质量：命名模糊，数据输入错误，数据丢失，数据格式不一致，缩写等  
  -  数据规模：数据量大，数据种类多样性，不再仅仅通过名字匹配，多种关系，更多链接等
3.	主要部分：本体对齐与实体匹配
4.	主要步骤：数据预处理，分块，负载均衡，记录链接，结果评估，结果输出	  
  (1)	数据预处理阶段：对不同来源的数据进行归一化处理  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a.  语法正则化：比如 保险公司名称的表示方法，各种保险条目的表示方式等  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.  数据正则化：用正式名字替换缩写，移除多余的空格，标点符号统一化等  
(2)	分块：从给定的知识库中的所有实体对中，选出潜在匹配的记录对作为候选项，并将候选项的大小尽可能的缩小  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a.  基于Hash函数分块：对于记录x，经hash函数hash(x)=hi,则x映射到与关键字hi绑定的块Ci上  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.  邻近分块：聚类，排序邻居算法等  
(3)	负载均衡：保证所有块中的实体数目相当，从而保证分块对性能的提升程度  
(4)	记录链接阶段：对于两个实体的记录，主要通过以下两步进行记录链接：  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a.  属性间的相似度：对应属性值之间  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;编辑距离：Levenshtein distance(最小编辑距离),Edit Distance with affine gaps等  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;集合相似度：Dice系数， Jaccard系数	需要将文本转化为集合  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;基于向量的相似度：TF-IDF算法  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.  实体间的相似度：实体对应的属性向量之间  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;聚合：将属性向量中对应向量的相似度进行 加权平均，手动制定规则等  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;聚类：层次聚类，相关性聚类等  
(5)	结果评估：准确率，召回率，F值等
5.	本体划分：依据概念间的结构亲近性计算  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a.  类的层次关系(父子类，公共父类等)，家庭财产保险是财产保险的一种，人寿保险是人身保险的一种  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b.  属性的层次关系,定义域关系等

 
