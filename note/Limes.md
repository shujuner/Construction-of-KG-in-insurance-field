Limes下载安装后，可以打包得到一个jar包。运行时主要是配置一个config.xml文件就可以。运行命令如下：  
cd target java -jar limes-core-1.0.0-SNAPSHOT.jar config.xml  
1 下面是一个配置文件实例  
<?xml version="1.0" encoding="UTF-8" standalone="no"?>  
 <!DOCTYPE LIMES SYSTEM "limes.dtd">  
 <LIMES>  
 <PREFIX>  
 <NAMESPACE>http://www.w3.org/2002/07/owl#</NAMESPACE>  
 <LABEL>owl</LABEL>  
 </PREFIX>  
 <PREFIX>  
 <NAMESPACE>http://geovocab.org/geometry#</NAMESPACE>  
 <LABEL>geom</LABEL>  
 </PREFIX>  
 <PREFIX>  
 <NAMESPACE>http://www.opengis.net/ont/geosparql#</NAMESPACE>  
 <LABEL>geos</LABEL>  
 </PREFIX>  
 <PREFIX>  
 <NAMESPACE>http://linkedgeodata.org/ontology/</NAMESPACE>  
 <LABEL>lgdo</LABEL>  
 </PREFIX>  
 <SOURCE>  
 <ID>linkedgeodata</ID>  
 <ENDPOINT>http://linkedgeodata.org/sparql</ENDPOINT>  
 <VAR>?x</VAR>  
 <PAGESIZE>2000</PAGESIZE>  
 <RESTRICTION>?x a lgdo:RelayBox</RESTRICTION>  
 <PROPERTY>geom:geometry/geos:asWKT RENAME polygon</PROPERTY>  
 </SOURCE>  
 <TARGET>  
 <ID>linkedgeodata</ID>  
 <ENDPOINT>http://linkedgeodata.org/sparql</ENDPOINT>  
 <VAR>?y</VAR>  
 <PAGESIZE>2000</PAGESIZE>  
 <RESTRICTION>?y a lgdo:RelayBox</RESTRICTION>  
 <PROPERTY>geom:geometry/geos:asWKT RENAME polygon</PROPERTY>  
 </TARGET>  
 <METRIC>geo_hausdorff(x.polygon, y.polygon)</METRIC>  
 <ACCEPTANCE>  
 <THRESHOLD>0.9</THRESHOLD>  
 <FILE>lgd_relaybox_verynear.nt</FILE>  
 <RELATION>owl:sameAs</RELATION>  
 </ACCEPTANCE>  
 <REVIEW>  
 <THRESHOLD>0.5</THRESHOLD>  
 <FILE>lgd_relaybox_near.nt</FILE>  
 <RELATION>owl:sameAs</RELATION>  
 </REVIEW>  
 <EXECUTION>  
 <REWRITER>default</REWRITER>  
 <PLANNER>default</PLANNER>  
 <ENGINE>default</ENGINE>  
 </EXECUTION>  
 <OUTPUT>TAB</OUTPUT>  
 </LIMES>  
配置文件中，<PREFIX>字段是定义的前缀空间缩写，<SOURCE>，<TARGET>字段是定义的数据源，就是比较这两部分数据源中实体之间的相似性。其中<ENDPOINT>字段是数据源的sparql终端地址，也可以是本地文件的绝对路径; <var>是用于比较的变量，而<RESTRICTION>则是对变量的一些限制条件。<METRIC>字段是距离度量函数，也可以使用一些机器学习算法来计算相似度。<ACCEPTANCE>是指接受条件，后面阈值为0.9，表示相似度大于等于0.9的可以认为是同一实体。<REVIEW>是复审条件，不满足接受条件的部分里面可能有实际上是同一实体的，将他们输出，用其他算法进行复审。这个配置文件中是使用的geo_hausdorff(x.polygon, y.polygon)距离来计算相似度  

运行结果  
十分接近的实体对  共424条实体对  
 
比较接近的实体对  共4070条数据  
 


接下来用余弦相似度Cosine进行测试  
	使用Cosine测试后，发现十分接近的实体对数量变为了290，而比较接近的实体对的数量变为了71528条  

使用机器学习算法进行测试  
![my](https://github.com/shujuner/Construction-of-KG-in-insurance-field/blob/guangxi/note/Picture/photot1.png)  

这里是使用的wombat simple算法，有监督批处理类型，使用ml_train_data.nt作为训练集来训练我们的算法，ml_train_data.nt文件内容如下:  
 
这里数据也是以三元组的形式存在，其中谓词都为sameAs，表示主体与客体表示同一个实体。  
最后运行结果显示，十分接近的实体对有4695对，而比较接近的为0。  

Limes有一个专门用于生成xml配置文件的网页，如下，在该网页中，我们输入前缀缩写，文件名，限制条件等信息，它可以自动的帮我们生成对应的xml文件。省去了一步步编写xml文件的繁琐步骤。  
 
 
