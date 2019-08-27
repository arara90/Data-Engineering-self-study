# Programming Hadoop with Pig

### Ambari -> pig view

[Problem]

Ambari에서 pig View가 구동되지 않는다. 원인은 WebHCat이라고 나옴.

[Solution]

https://community.cloudera.com/t5/Support-Questions/Unable-to-view-the-Pigview-from-apache-ambari/m-p/121876

1. admin으로 로그인 되었는지 확인한다.

   (비밀번호 모르는 경우 ) su root -> ambari-admin-password-reset 로 재설정 

2. 상단 Hosts로 들어가서 WebHcat Server가 Started 상태인지 확인한다. 

![그림 3-2](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_002.png?raw=true)

### Why Pig ?

* writing mappers and reducers by hand takes a long time.
* SQL-like syntax to define map and reduce steps.
* Highly extensible with user-defined functions(UDF's)



##### running on top of Tez

up to 10 times faster than running on top of mapreduce 

![그림3-3](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_003.png?raw=true)



#### Tez? 

it's basically a much more efficient way of **organizing these job**s so it runs what's called a **directed acyclic graph**.

So with **mapreduce you have sort of this fixed chain of events** that happened you know you have a mapper and a reducer that feeds into another mapper and reducer that feeds into another mapper and reducer In sort of this linear manner.

**Tez **can actually look at the interdependencies(상호의존) between the things you're trying to do, and **compute the optimal path** for getting it done.

So by going through Tez you can often find that things run you know in my experience up to about 10times **faster than they would on top of mapreduce**.



### Running Pig

Grunt : command line interpreter

Script 

Ambari / Hue



#### Example - Find the oldest 5-star movies

* Create a relation names ratings with a given schema 

```
ratings = LOAD '/user/maria_dev/ml_100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);
```



* use **PigStorage** if you need a different **delimiter**(구분자)

  * USING PigStorage('|')  

  * DUMP metadata : 명시한 데이터만 보여줌. (Anything that is not part

    of our explicit schema just gets discarded )

```
metadata = LOAD '/user/maria_dev/ml_100k/u.item' USING PigStorage('|') AS (movieID:int, movieTitle:cjararray, releaseDate:chararray, videoRelease:chararray, imdbLink:chararray);

DUMP metadata; 
```

​	

* Creating a relation from another relation ; **FOREACH / GENERATE - Transform**
  * FOREACH로 하나씩 row를 꺼내와서 GENERATE로 새로운 row을 생성

```
metadata = LOAD '/user/maria_dev/ml_100k/u.item' USING PigStorage('|') AS (movieID:int, movieTitle:cjararray, releaseDate:chararray, videoRelease:chararray, imdbLink:chararray);

nameLookup = FOREACH metadata GENERATE movieID, movieTitle, ToUnixTime(ToData(ReleaseDate, 'dd-MMM-yyyy')) AS releaseTime;
```



* **Group BY** - like Reducer

```
ratingsByMovie = GROUP ratings BY movieID;
DUMP ratingsByMovie
```

​	ratingsByMovie = { group = movieID ,ratings = {나머지} } 



* **AVERAGE** rating relation

```
avgRatings = FOREACH ratingsByMovie GENERATE group AS movieID, AVG(ratings.rating) AS avgRating;
DUMP avgRatings

DESCRIBE ratings;
DESCRIBE ratingsByMovie;
DESCRIBE avgRatings;
```

![그림3-4](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_004.png?raw=true)

* **FILTER**

```
fiveStarMovies = FILTER avgRatings BY avgRating > 4.0;
```

*  **JOIN**

```
DESCRIBE fiveStarMovies;
DESCRIBE nameLookup;
fiveStarsWithData = JOIN fiveStarMovies By movieID, nameLookup By movieID;
DESCRIBE fiveStarsWithData;
DUMP fiveStarsWithData;
```

![그림3-5](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_005.png?raw=true)

(컬럼명만 보면)

fiveStarsWithData = { movieID, avg, movieID, movieTitle, releaseTime }



* **ORDER BY**

```
oldestFiveStarMovies = ORDER fiveStarsWithData BY nameLookup::releaseTime;
```



* **Putting all Together**

```
ratings = LOAD '/user/maria_dev/ml-100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);
metadata = LOAD '/user/maria_dev/ml-100k/u.item' USING PigStorage('|')
	AS (movieID:int, movieTitle:chararray, releaseDate:chararray, videoRealese:chararray, imdblink:chararray);
   
nameLookup = FOREACH metadata GENERATE movieID, movieTitle,
	ToUnixTime(ToDate(releaseDate, 'dd-MMM-yyyy')) AS releaseTime;
   
ratingsByMovie = GROUP ratings BY movieID;
avgRatings = FOREACH ratingsByMovie GENERATE group as movieID, AVG(ratings.rating) as avgRating;
fiveStarMovies = FILTER avgRatings BY avgRating > 4.0;
fiveStarsWithData = JOIN fiveStarMovies BY movieID, nameLookup BY movieID;
oldestFiveStarMovies = ORDER fiveStarsWithData BY nameLookup::releaseTime;
DUMP oldestFiveStarMovies;
```



#### RUN

* Pig view -> script -> excute 

![그림3-6](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_006.png?raw=true)





* Runinng......

![그림3-7](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_007.png?raw=true)

* Result.....

![그림3-8](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_008.png?raw=true)



* run it FASTER (check On TEZ)

![그림3-9](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_009.png?raw=true)



​																							▼ On top of Tez ( 3분 -> 45초)



![그림3-10](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/3_1_pig/3_010.png?raw=true)



### Pig Latin : Diving Deeper Things you can do to a relation

* **LOAD , STORE  , DUMP**

  * STORE ratings INTO 'outRatings' USING PigStorage(':');

    STORE [relation name] INTO ['file name'] USING PigStorage(['delimiter']);

    

* **FILTER , DISTINCT , FOREACH/GENERATE , MAPREDUCE , STREAM , SAMPLE**

  * **FILTER** : Filter things out into a relation based on some boolean expression that you set up.

  * **DISTINCT** : Distinct gives you the unique values within a relation for each generate we've

    looked at basically a way of creating a new relation from an existing one going through a one line at

    a time and transforming it in some way.

  * **MAPREDUCE** : It was actually lets you call explicit mappers and reducers on a relation. So you don't have to choose between Pig and mapreduce. you can actually blend the two togethe

  * **STREAM** : It's also used for extensibility. You can actually **stream the results of Pig out to a process** and just use standard in and standard out, just like a mapreduce streaming does.

  * **SAMPLE** : sample can be used to **create a random sample** from your relation.

    

* **JOIN , COGROUP , GROUP , CROSS , CUBE**

  * **JOIN** 

  * **?? COGROUP** is just a variation of join So, whereas join puts the resulting joined rows together into a single tuple, **cogroup actually creates a separate tuple for each key**

    -> 각각의 유일한 그룹 키마다 하나의 튜플을 생성한다.  튜플의 첫 번째 항목은 키고. 나머지 항목은 일치하는 키를 가지는 각 관계자로부터 생성된 튜블의 백이다.

    첫번째 백은 관계자 A에서 같은 키를 가지는 튜플을 담고있고, 두번째 백은 관계자 B에게서 같은 키를 가지는 튜플을 담고 있다. 

  

   

  

  

  

  

  * and **it creates this nested structure.** So it's a little bit **more organized** than what joined gives you so you have the choice between the two.\

  * 이후의 문장에서 그 구조를 활용하고자 할 때 유용하다.

    

    

  * **GROUP** 

  * **CROSS** lets you do all the combinations between two relations. This is also called the **Cartesian product.** 

  * **CUBE** can take more than two columns and do all the combinations between them as

    well. 

  * 

* **ORDER , RANK , LIMIT**

  * **ORDER** 

  * **RANK**  : Rank is like order but instead of ordering, it actually **assigns a rank number to each row.**

  * ??**LIMIT** : This comes in handy sometimes especially while debugging. So it's a way of just taking back the first and results from a relation.

    So if you're just experimenting or debugging something you can say limit whatever your relationship, whatever your relation name is.

    If you don't want to dump the entire thing out, you can create a new relation using limit and then dump out the first,

  * 

* **UNION , SPLIT**

  * **UNION**  : 

  * **SPLIT** :

    