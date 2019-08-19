## Overview of the Hadoop Ecosystem

![img2-14.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-14.png?raw=true)

------



### Core Hadoop Eco-System

![img2-11.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-11.png?raw=true)

The pink things here are the things that are part of Hadoop itself.



#### HDFS

- HDFS is the system that allows us to **distribute the storage of big data across our cluster of computers** so it makes all of the hard drives on our cluster look like one giant file system.

  So if one of your computers happens to randomly burst into flames and melts into a puddle of silicon it happens - it can actually recover from that and it will back itself up to a backup copy that it had of that data automatically. So that's the power of HDFS.



#### YARN - stands for Yet Another Resource Negotiator.

-  YARN is where the data processing starts to come into play.

- So YARN is basically the system that **manages the resources on your computing cluster**.
  - It's what decides what gets to run tasks when what nodes are available for extra work which nodes are not which ones are available which ones are not available so it's kind of the the heartbeat that **keeps your cluster going.**



#### MapReduce  

- **Mappers** have the ability to **transform your data in parallel across your entire computing cluster** in a very efficient manner.

- **Reducers** are what **aggregate that data together** and it may sound like a very simple model, but it's actually very versatile.
- Now originally map reduce and YARN were kind of the same thing in Hadoop. They got split out recently and that's enabled other applications to be built on top of yarn that solve the same problem as map reduce but in a more efficient manner.



#### Pig

- Pig is a very high level programming API that **allows you to write simple scripts that look a lot like SQL** in some cases that allow you to chain together queries and get complex answers but without actually writing Python or Java code
- in the process so Pig will actually transform that script into something that will run on map reduce which in turn goes through yarn and HDFS to actually process and get the data that it needs to get the answer you want. 



#### Hive

-  it solves a similar problem to pig but it really more directly

- looks like a SQL database, so Hive is a way of **actually taking SQL queries** and making this distributed data that's just really sitting on your file system somewhere look like a SQL database.

  

#### Apache Ambari

- Apache Ambari is basically this thing that sits on top of everything.

- It just gives you a v**iew of your cluster and lets you visualize** <u>what's running on your cluster</u>, <u>What</u>

  <u>systems are using</u>, <u>how much resources</u> and also **has some views in it that allow you to actually do things** like <u>execute hive queries</u> or <u>import databases into hive</u> or <u>execute Pig queries</u> and things like that.

- Now there are other technologies that do this for you and Ambari is what Hortonworks uses. There are competing distributions of Hadoop stacks out there, Hortonworks being one of them. 

- Other ones include Cloudera and MapR but for Hortonworks they use Ambari.

  

#### Mesos

- Mesos **isn't really part of Hadoop proper** but It belongs to here, because it's basically

  an **alternative to yarn**.

- Mesos is **another potential way of managing the resources** on your cluster. (cf. YARN)

- There are ways of getting Mesos and YARN to work together if you need to as well.

  

#### Spark

- this is sitting at the same level of map reduce in that it sits on top of yarn or Mesos 

- it can go either way to actually **run queries** on your data 

  and like **MapReduce** it requires some programming and need to actually write your **SPARK scripts using either Python or Java or the Scala programming language** Scala being preferred.

- So if you **need to very quickly and efficiently and reliably process data on your cluster** SPARK is a really good choice for that.

  And it's **also very versatile** it can do things like **handle SQL queries** that **can do machine learning**

  **across an entire cluster of information**.

  It can actually **handle streaming data in real time** and all sorts of other cool stuff.

  

#### Tez

- Tez similar to spark in that it also uses some of the same techniques as SPARK notably with

  something that's called a **directed acyclic graph** and this gives Tez a leg up on what map reduce does, because **it can produce more optimal plans for actually executing queries**. 

  > **Directed Acyclic graph**
  >
  > <https://steemit.com/dag/@cryptodreamers/dag-dag-directed-acyclic-graph>
  >
  > [순환그래프]
  >
  > ![áá³áá³ááµá«áá£áº 2018-03-23 áá©áá® 11.07.31.png](https://steemitimages.com/640x0/https://steemitimages.com/DQmUJaKxfxSgvZwWyfxvMv74UT3qZeHP6Ewoo6EgbhWgpuo/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202018-03-23%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2011.07.31.png)
  >
  > [비순환그래프]
  >
  > 
  >
  > ![](https://steemitimages.com/DQmR2YCjhtSzW5DfpraEjRLfqyzcAVdtBY74CBEkuRYiXve/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202018-03-23%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2011.53.14.png))
  >
  > 
  >
  > 계속적으로 순환될 수 있는 구간이 없기 때문에, 순환그래프에서 발생하는 문제점들이 없다는 것이죠! 
  >
  > 이를 위상정렬이라고 표현합니다(Topologically sorted). 
  >
  > 
  >
  > **DAG(Directed Acyclic Graph)는 일방향성만 가지는 그래프입니다.**
  >
  > (비가역적 일방향성 -> 블록체인의 핵심적인 특성)
  >
  > ![](https://steemitimages.com/640x0/https://steemitimages.com/DQmak85ECZtWk19JX5cve5osCdUoaKYtgG7WSBG2M1iMAoM/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202018-03-24%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%2012.21.17.png)

  

- Tez is usually used in conjunction with Hive to accelerate it. So we remember we looked at hive earlier that kind of sat on top of map reduce but it can also sit on top of Tez.

  So you have an option there high through Tez can often be faster than high through map reduce.

  Both different means of optimizing queries to get a efficient answer from your cluster.



#### HBASE

-  it's a way of **exposing the data on your cluster to transactional platforms** so HBase is what we call a **NoSQL database**, columnar data store.

- It's basically a really **fast** database meant for very **large transaction** rates 
  - so it's appropriate for example for hitting from a web application hitting from a Web site doing all types of transactions 
- so HBase can actually expose the data that's stored on your cluster and maybe that data was transformed in some way by spark or map reduce or something else.
- it provides a very fast way of exposing those results to other systems.



#### APACHE STORM

- Storm is basically a way of processing **streaming data**.
- Spark streaming solves the same problem. Storm just does it in a slightly different way.
- You can actually update your machine learning models or transform data into a database all in real time as it comes in.



#### Oozie

- Oozie is just a way of scheduling jobs on your cluster.

- So when you have more complicated operations that require <u>loading data into hive</u> and then <u>integrating that with Pig</u> and maybe <u>querying it with SPARK</u> and then <u>transforming the results into HBase</u>, **Oozie can manage that all for you and make sure that it runs reliably on a consistent basis.**

  

#### Zookeeper

- t's basically a technology for coordinating everything on your cluster.

- it's the technology that **can be used for keeping track of which nodes are up which nodes are**

  **down**. It's a very reliable way of **keeping track of shared states across your cluster** that

  different applications can use and many many of these applications we've talked about rely on zookeeper to **actually maintain reliable and consistent performance across the cluster.**

  Even when a node randomly goes down.

  So zookeeper can be used for example for keeping track of who the current master node is or keeping track of who's up who's down what have you.



#### Data Ingestion

- How do we actually get data into your cluster and onto HDFS from external sources.

- **SQOOP** : is a way of actually **tying your Hadoop database into a relational database**. Anything that can talk to ODBC or JDBC can be transformed by Sqoop into your HDFS file system.

   so Sqoop is basically a **connector** between Hadoop and your legacy databases. 

- **Flume** : It's a way of actually **transporting Web logs** at a very large scale and very reliably to your cluster.

  So let's say you have a fleet of web servers, Flume can actually listen to the web logs coming in from those web servers in real time and publish them into your cluster in real time for processing by something like storm or spark streaming.

- **Kafka** : Kafka solves a similar problem although it's a little bit **more general purpose**.

  It can basically **collect data of any** from <u>a cluster of PC</u>s from <u>a cluster of web servers</u> or <u>whateverit</u> is **and broadcast that into your Hadoop cluster** as well.

  

------

### External Data Storage

![img-12.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img-12.png?raw=true)



Your data might be exposed or stored in **other places** too.

**HBase** would also fit into this category. But since HBase is really part of the Hadoop stack itself.

So, It is left off of this little collection here.



#### MySql

- MySQL of course or any SQL database is something you might be integrating with your cluster or

  you can not only import data from Sqoop into your cluster, You can also export it to MySQL as well

- A lot of these technologies like Spark have the ability to write to any JDBC or ODBC database and

  you can store and retrieve your results from a central database.



#### cassandra

- Columnar data store which is good choices for exposing your data for real time usage to say a web application.



#### mongoDB

- Columnar data store which is good choices for exposing your data for real time usage to say a web application.



------

### Query Engines

![img-13.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img-13.png?raw=true)

if you want to actually interactively enter SQL queries or whatever you can do that using these technologies. 

Hive that actually is a similar thing as well. But again since Hive is more tightly integrated into Hadoop, let's leave it out of this particular circle but it too is a way of querying your data.



#### Apache Drill

- It actually allows you to **write SQL queries** that will work across a wide range of **NoSQL databases**

  potentially so they can actually talk to your HBase database and maybe your Cassandra and your MongoDB as well.

- Tie those results all together and allow you to **write queries across all those disparate data stores** and bring them all back together when you're done.

  

#### Hue

- A way of interactively creating queries that works well with hive and hbase.

- Actually for Cloudera it takes the role of Ambari as sort of the thing that sits on top of everything and **lets you visualize and execute queries** on the Hadoop cluster as a whole.



#### Apache Phoenix

- Phoenix is similar to drill, it lets you do **SQL style queries across the entire range of data storage** technologies you might have 

- But it takes it **one step further it actually gives you ACID guarantees and OLTP.**

  So you can actually make your not SQL Hadoop data store look a lot like a relational data store in a relational database with all the guarantees that come with that.

  

#### presto

- presto yet another way to **execute queries across your entire cluster.**
- These all solve you know kind of the same problem.



#### Apache Zepplin

- Zeppelin is just another angle on it that takes more of a **notebook type approach to the UI** and **how you actually interact with the cluster.**

  