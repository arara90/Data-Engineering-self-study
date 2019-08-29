# Hive

### Hive?  Distributing SQL queries with Hadoop

![5_001.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_001.png?raw=true)

* It is really powerful stuff, if you're already familiar with SQL.

* Let you write standard SQL queries, but actually execute them on data that's stored across entire cluster.
  * Translating SQL into **MapReducer** or **Tez** 
  * Runs on top of the Hadoop **YARN** cluster manager.



### Why Hive?

![5_002.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_002.png?raw=true)

The familiarity of it is the main key,  it allows you to leverage that knowledge to become very quickly productive using a Hadoop cluster.

It's actually called **HiveQL**, which is a variant of SQL, and it's very similar to MySQL syntax.



* It's **scalable**

  * It can actually work with data that's distributed on an entire cluster of computers, unlike a traditional database, where you're restricted to what you can fit on one single host.

  * It's a powerful tool for data-warehouse types of applications where you're trying to

    issue a query on a very large dataset.

  * OLAP ( Online Analytics Processing)에 적합, not OLTP(Online Transaction Processing)

  

* it's highly **extensible**

  * If SQL is not enough for you, you can plug in your own **user-defined functions**.

    

* it **exposes the Thrift server**

  * you can talk to Hive from a service outside of Hive.

    > Thrift server allows external clients to interact with Hive over a network, similar to the [JDBC](https://en.wikipedia.org/wiki/Jdbc) or [ODBC](https://en.wikipedia.org/wiki/Odbc) protocols.
    >
    > Ref. [Wikipedie-Apache Hive](https://en.wikipedia.org/wiki/Apache_Hive#cite_note-22)

  *  It exposes the JDBC and ODBC driver to make Hive look just like any other database.

  *  So There are lots of ways to **extend** Hive and lots of ways to **work it into other systems**.



### Why not Hive?

![5_003.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_003.png?raw=true)



* It's **not for OLTP**(Online Transaction Processing), for OLAP

  * "High throughput, low latency" - Hive isn't going to cut it.

    > [Throughput ](http://terms.naver.com/alikeMeaning.nhn?query=88206260) :  단위 시간당 컴퓨터 시스템이 처리할 수 있는 작업의 수
    >
    > [Latency](https://terms.naver.com/entry.nhn?docId=2763103&cid=50307&categoryId=50307)  : 지연 속도, 네트워크에서 하나의 데이터 패킷이 한 지점에서 다른 지점으로 보내지는 데 소요되는 시간.

  * it's going to be translating SQL commands into MapReduce jobs, and MapReduce jobs take some time to spin up.

    

* Stores data **de-normalized** 

  * it's not a real relational database under the hood, **it's just flat text files**. Everything's de-normalized.

  * If you do need to do more **complicated queries**, then something like **Pig** or **Spark** might be more appropriate.

    

* No Transactions, No record-level updates, inserts or deletes..

  * It's just big flat text files that you're chugging through with mappers and reducers(it's just MapReduce under the hood)

  

### HiveQL

![5_004.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_004.png?raw=true)



HiveQL은 Hive에서 사용하는 변형된 형태의 SQL이다. 따라서 MySQL과 매우 유사하다. 하지만 Hive만 가지고 있는 Extension들과 Exception(like record-level stuff)들도 존재한다.



#### Extension

* **View**

  *  You can store the results of one query into a view and then use that view as a table in subsequent queries.

  * It's not quite the same thing as a materialized view(stores copies of the data) in the database world.

    A **view in Hive is** more of a **logical construct**, so that logical construct of a view will **persist**, but it's **not actually storing a copy of the data anywhere**.

    

#### Exception

HiveQL has a bunch of extensions to allow you to specify exactly how the data is structured and stored and partitioned.





### Exercise

Hive View

![5_005.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_005.png?raw=true)

Query 

​	Drop Table -> refresh 후 확인

![5_006.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_006.png?raw=true)



Upload Table

* u.data

  ![5_007.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_007.png?raw=true)

  ![5_008.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_008.png?raw=true)

Delimiter 설정 -> 9 Tab

Table name : ratings

Columns : userID(Int), movieID(Int), rating(Int), epochseconds(Int)





u.item

Delimiter 설정 -> 124 ('|')

![5_009.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_009.png?raw=true)

Table name : names

Columns : movieID(Int), title(String)



#### Query 작성

![5_010.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_010.png?raw=true)

```sql
CREATE VIEW IF NOT EXISTS topMovieIDs AS
SELECT movieID, count(movieID) as ratingCount
FROM ratings
GROUP BY movieID
ORDER BY ratingCount DESC;

SELECT n.title, ratingCount
FROM topMovieIDs t JOIN names n ON t.movieID = n.movieID;
```



#### DROP VIEW

![5_011.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_011.png?raw=true)