# Hive

## How hive works? 


### Schema on read

* **RDB - schema on write** : 데이터를 로드하기 전에 스키마를 미리 정의해 놓으며, 데이터를 디스크에 저장한다.

* **Hive - schema on read** : 구조화되지 않은 데이터를 다루고, 데이터를 읽을 때 스키마를 적용한다. 따라서 데이터 구조와는 상관없이 텍스트 파일 그대로 저장되어있다.  하이브는 actual schema data 라고 불리는 **metastore**가 이 텍스트 파일을 어떻게 interpret할 것인지에 알려준다. 이것을 Schema on read라고 부른다.

* **HCatalog** : 다른 서비스에 이 스키마를 보여준다.
* 

> Relational database uses something called **schema on write**, where you define the schema of your database before you load the data into it, and it's enforced at the time that you write the data to disk.
>
> Hive flips that on its head.
>
> It takes unstructured data and applies a schema to it as it's being read instead. So your data is still stored as just tab-delimited text files or whatever with no actual structure, no actual information about kind of data that represents. 
>
> But Hive maintains a **metastore** called the actual schema data. That's associated with that unstructured data, so that's what tells it how to actually interpret those raw text files. 
>
> it's called **schema on read**, and it's a separate product called **HCatalog** that can expose that schema to other services as well.



```sql
CREATE TABLE ratings(
    userID INT,
    movieID INT,
    rating INT,
    time INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;	--Create a schema in the metastore 

LOAD DATA LOCAL INPATH '${env:HOME}/ml-100k/u.data' -- Copy data from LFS to Hive
OVERWRITE INTO TABLE ratings;
```



### Where is the data?

![5_013.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_013.png?raw=true)

* **LOAD DATA - MOVE DATA FROM DFS**

  * Takes ownership of data and **MOVES data from a Distributed file system into Hive.**

  *  **Reason** why Hive **moves the data** : DFS에 거대한 데이터를 갖고 있다면 또다른 복사본을 원치 않을 가능성이 크다 (Big Data니까! ). 따라서 Hive는 copy가 아니라 Hive가 놓여있길 원하는 곳에다가 데이터를 Move하고, 소유권을 갖는다.

    > Reason being that if you have a massive dataset on its distributed file system, odds are you don't really want another copy of it.  So Hive is just going to move that to where Hive expects it to be, and Hive will take ownership of that data from now on. 



* **LOAD DATA LOCAL - COPY DATA FROM LFS**

  * **COPIES data from your local file System into Hive**

  * Local에 저장할만한 데이터라면 빅데이터가 아니라고 암시적으로 가정함. 따라서 복사본을 만들고 Ownership을 갖는다. 

    

* **Managed vs External tables**

  * **MANAGED TABLE** : Hive가 Ownership을 가진다. 

    * Drop시 데이터도 사라진다.

      

  * **EXTERNAL TABLE** 

    * Hive 외 다른 시스템과 해당 데이터를 공유하고자 할 때
    * Hive doesn't take ownership of data.
    * "CREATE EXTERNAL TABLE" with "LOCATION" : "I'm going to use Hive on this data here, but I'm not going to own it anymore" 즉, 해당 데이터를 하이브가 사용 하되, 소유하지는 않는다.
    * DROP 시 데이터는 온전하게 남아있는다.

    ```sql
    CREATE EXTERNAL TABLE IF NOT EXISTS ratings(
        userID INT,
        movieID INT,
        rating INT,
        time INT)
    ROW FORMAT DELIMITED FIELDS TERMICATED BY '\t'
    LOCATION '/data/ml-100k/u.data' 
    ```

    

### Partitioning

![5_014.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_014.png?raw=true)

 PARTITIONED BY 에 쓰이는 컬럼처럼 보이지만, 컬럼이 아니라 해당 데이터를 저장해 놓은 곳에 subdirectory를 만든다. 즉, '../customers/country=CA'는 customers 테이블에 country가 CA인 데이터이다.  체인 형식으로도 만들 수 있다.('../customers/country=CA/province=Alberta')

  캐나다에 사는 customer를 조회하고 싶으면 바로 해당 디렉토리에 가서 데이터를 스캔하면 되므로 많은 시간을 절약할 수 있다. 

> If you say "PARTITIONED BY (country STRING)", that treats "country" as just another column**, but it's not really a column under the hood.** The "country" column will become **part of a subdirectory** under where Hive stores this data.



### STRUCT

하이브 db에 INT, STRINGS, BYTE와 같은 일반적인 데이터 타입을 저장하도록 제한하지 않고, map이나 구조화된 데이터 타입도 저장할 수 있다. 



### Ways to use Hive

![5_015.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/5_Hive/5_015.png?raw=true)

* OLTP는 HBASE를 고려할 것. (웹 사이트같이 동시다발적으로 쿼리들이 발생하는 경우)

* Oopzie : Oozie is a **management tool** for your cluster as a whole that lets you **schedule more complicated jobs across your Hadoop cluster**.



### [Exercise]

* Find the movie with the highest average rating
* Extra credit : only consider movies with more than 10 ratings

*  Remember, your views are persistent, they're stored to disk, and if you actually try to create the same view more than once, you will get an error, so if you start running into that, remember to drop your view in between runs, OK?

```sql
CREATE VIEW IF NOT EXISTS avgRatings AS
SELECT movieID, AVG(rating) as avgRating, COUNT(movieID) as cntRating
FROM ratings
GROUP BY movieID
ORDER BY avgRating DESC;

SELECT n.title, r.avgRating
FROM avgRatings r JOIN names n ON r.movieId = n.movieID
WHERE r.cntRating > 10;
```

