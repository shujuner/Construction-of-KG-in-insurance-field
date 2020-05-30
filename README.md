                       
## ***SPARQL_Engine***
用到的一些SPARQL引擎。
1.	HadoopRDF: 一种基于垂直分区思想的SPARQL引擎。HadoopRDF在HDFS上使用多个文件存储数据，每个谓词对应于一个文件，还基于显式和隐式类型信息将每个谓词文件分割为多个更小的文件。HadoopRDF以MapReduce迭代序列的形式执行查询。它包含一个查询优化器，用于选择最小化MapReduce迭代次数和中间结果大小的查询计划。 
2.	S2RDF: 基于Spark的SPARQL引擎，它提出了一种用于RDF数据的关系分区技术，称为扩展垂直分区(ExtVP)。ExtVP扩展了HadoopRDF使用的垂直分区方法，以便在查询计算期间最小化输入数据的大小。ExtVP使用半连接约化来最小化数据偏差，并消除不参与任何连接的悬浮三元组。对于任意两个垂直分区，ExtVP预计算连接缩减，结果在HDFS中物化为表。这样做的目的是使用半连接简化表代替原本的基表，因为简化表要小得多。S2RDF不直接在Spark上运行，它将SPARQL查询转换为SQL作业，然后使用Spark SQL进行执行。
3.	SparkRDF:基于Spark的SPARQL引擎。它使用哈希分区将图分布到多层弹性子图(MESG)中。MESG是基于类和关系来减少搜索空间与内存开销的。在SparkRDF中创建了五种索引，用于建模RDSGs(弹性离散子图)。对于查询处理，SparkRDF使用Spark api和迭代连接操作来最小化中间结果，以执行子图匹配。

4.	S2X利用RDFh数据内在的图结构，将SPARQL查询作为基于图的计算在GraphX上进行处理。它使用并行的顶点中心模型来执行SPARQL的BGP匹配，而其他的操作符，如可选和过滤，则通过Spark-RDD操作符进行处理。BGP匹配首先将所有三元组模式分不到所有图顶点，每个顶点的标签都与三元组的谓词进行匹配。图顶点与他们的直接邻居顶点通过信息交换协同验证其三重候选性。然后，收集部分结果并增量合并。S2X使用两种字符串编码类型:散列和基于计数的编码。基于哈希的编码使用64位哈希函数对主体和对象进行编码，而基于计数的编码则为它们分配唯一的数值。S2X没有特殊的RDF分区器，它使用GraphX散列来将输入图在工作节点之间进行分区。

5.	SPARQLGX以垂直分区的方式将RDF数据存储在HDFS中，具有快速转换、压缩存储和轻量级索引等优点。查询时基于VP表以及一些统计信息，将SPARQL查询转化为可执行的scala代码。

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

 
