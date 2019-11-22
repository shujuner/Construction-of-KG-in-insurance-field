Limes的使用
===========
1.  Limes下载安装后，可以打包得到一个jar包。运行时主要是配置一个config.xml文件就可以。运行命令如下：  
cd target java -jar limes-core-1.0.0-SNAPSHOT.jar config.xml  
    
    
2. 下面是一个配置文件实例  
![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/a.png)
![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/b.png)  

配置文件中，```<PREFIX>```字段是定义的前缀空间缩写，```<SOURCE>```，```<TARGET>```字段是定义的数据源，就是比较这两部分数据源中实体之间的相似性。  
其中```<ENDPOINT>```字段是数据源的sparql终端地址，也可以是本地文件的绝对路径; ```<var>```是用于比较的变量，而```<RESTRICTION>```则是对变量的一些限制条件。```<METRIC>```字段是距离度量函数，也可以使用一些机器学习算法来计算相似度。```<ACCEPTANCE>```是指接受条件，后面阈值为0.9，表示相似度大于等于0.9的可以认为是同一实体。```<REVIEW>```是复审条件，不满足接受条件的部分里面可能有实际上是同一实体的，将他们输出，用其他算法进行复审。这个配置文件中是使用的```geo_hausdorff(x.polygon, y.polygon)```距离来计算相似度  
  
  
运行结果如下：  
十分接近的实体对  共424条实体对  
 ![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/c.png) 
比较接近的实体对  共4070条数据  
 ![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/d.png) 
  
  

3. 接下来用余弦相似度Cosine进行测试  
	使用Cosine测试后，发现十分接近的实体对数量变为了290，而比较接近的实体对的数量变为了71528条  
  
  
4. 使用机器学习算法进行测试  
![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/photot1.png)  
这里是使用的wombat simple算法，有监督批处理类型，使用ml_train_data.nt作为训练集来训练我们的算法，ml_train_data.nt文件内容如下:  
![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/photot2.png)  
这里数据也是以三元组的形式存在，其中谓词都为sameAs，表示主体与客体表示同一个实体。  
最后运行结果显示，十分接近的实体对有4695对，而比较接近的为0。  

5. Limes有一个专门用于生成xml配置文件的网页，如下，在该网页中，我们输入前缀缩写，文件名，限制条件等信息，它可以自动的帮我们生成对应的xml文件。省去了一步步编写xml文件的繁琐步骤。  
 ![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/photo3.png)<br>
 
 ![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/photo4.png)<br>
 
 ![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/photo5.png)<br>
 
 ![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/photo6.png)<br>
