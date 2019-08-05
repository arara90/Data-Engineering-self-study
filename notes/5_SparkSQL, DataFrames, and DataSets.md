# 5. SparkSQL, DataFrames, and DataSets

* 스파크에서 점점 중요해지고 있는 파트.
*  구조화되지 않은 RDD(Resilient Distributed Dataset)들을 구조화 시키고, DB처럼 다룰 수 있다.
* 이러한 구조화된 Dataset을 'DataFrame' 그리고 'DataSets'라고 부르자.
* DataFrame
  * Contain Raw Objects
  * Can run sql queries -> Spark can actually do optimiztion(최적화가능!)
  * Has a **schema** (leading to more efficient storage)
  * Read  and write JSON, Hive, parquet
  * Communicates with JDBC/ODBC, Tableau

* DataSet
  * In spark 2.0, a DataFrame is really a DataSet of Row Objects.
  * Dataset은 일반적으로 알려지고, 규정된(typed) 데이터를 Wrap할 수 있다. 하지만 파이썬은 untyped되어 있기 때문에 우리는 인식할 수 없다.(transparent to you in Python.)\
  * 너무 깊게 생각할 것 없이 Spark 2.0에서는 가능하면 DataFrame대신 DataSets를 사용한다.

* Shell Access : 

  * Spark SQL exposes a JDBC/ODBC server. ( if you built Spark with Hive support) 

  * port 10000 by default

  * Connect using bin/beeline -u jdbc:hive2://localhost:10000

  * Viola, you have a SQL shell to Spark SQL

  * You can create new tables, or query existing onew that were cached using hiveCtx.cacheTable("Name")

     

* Spark SQL이 직관적인것처럼 보이지는 않지만, High level API로서 스파크가 좀 더 optimization할 수 있는 기회를 제공하여 더 빠르고, 효율적이다.



## Datasets

Dataset is just a DataFrame of structure.

So, when people talk about datasets, they're really talking about DataFrame Full of Structure data, and more accurately, a DataFrame is a DataSet of row objects.

DataFrame은 Row objects의 DataSet이다?

So, DataFrame is not a DataSet.



So again DataSets are the way of the future in Spark 2.0.

You're gonna see that it's being used more widely as a common interface between the different components of Spark, 

so **MLlib** now has a DataSet based API, **Spark streaming** has a DataSet based API, so DataSets

are a very important concept to understand especially a Spark develops in the future.





# 실습

1. sparkSession
2. road unstructured data
3. mapper -> creates Row objects where where we're actually giving some structure here





# QnAs

**DataFrame vs DataSet confusion?** - **[Goraj](https://www.udemy.com/user/gunvant-kathrotiya/)**    

In previous lecture frank mentioned use dataset over dataframe then why in this example we're creating dataframe and not dataset?



Hello Goraj,

Both are similar, DataSet is strict in that you need to code the column types in development time which is good in case you want to make your code type safe.

If type safety is not a concern, you can use DataFrames as you already know the row columns structure.

Regards