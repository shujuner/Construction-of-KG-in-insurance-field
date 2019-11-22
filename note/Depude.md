Depude
=======
Dedpue是一个python包，在知识融合领域有着重要作用，其主要是用来实体匹配。  
Dedupe基于active learning, 在运行过程中，会将其不能做出判断的样本打印出来让人工判断。即其返回结果有三种：y(重复)，n(不重复)，u(不确定)。

下面是一个使用dedpue去重的具体实例：  
运行脚本之后，首先是active learning阶段，这里 程序中会向我们展示一系列的实体以及他们的特征，这里需要对他们是否为同一实体做出判断，程序根据我们在这里的判断决定程序判断时所使用的参数等。
运行完后会生成csv_example_learned_settings，csv_example_training.json， csv_example_output.csv 这3个文件。这里csv_example_output.csv就是预测结果文件。csv_example_learned_settings是根据用户标注数据训练好的模型，如果当前程序中有该文件，则直接加载模型，不再训练；如果没有该文件，则进行训练。 
Dedpue根据下面的fields字段进行测试，判断两个实体是否为同一个，对于String类型数据，采用affine gap string distance去对比。  
![image](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/depude1.png)
 
Depude会在运行期间，将其不能判断的样本打印出来，让用户自行判断
Depude使用准确率与召回率来对结果进行综合判断
实验结果如下：
 ![image](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/depude2.png)  
 ![image](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/depude3.png)  
 ![image](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/depude4.png)
 
 


depude本质上是“去重”，其核心方法就是通过各种数据类型（fields中的数据类型）来对样本进行比较计算相似度，然后通过聚类，进而达到将重复的数据（叫做同一类也好）聚集到同一类下，最终实现去重的目的，可以将这一思想应用的各个方面，类如包括连接两个表，专利消除歧义等等吧。Depude基于active learning, 需要首先人工判断一些数据，且这部分将作为我们算法的训练模型，所以，为了实现更高的正确率，我们应该做更多，更正确的人工判断，这也是其麻烦之处。
