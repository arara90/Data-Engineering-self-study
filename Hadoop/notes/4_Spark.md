# Spark

* Spark 폴더에 자세하게 정리

![4_001.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/4_Spark/4_001.png?raw=true)

## RDD

### Creating RDD

nums = parallelize([1,2,3,4])

sc.textFile("file://" or "s3n://" or "hdfs://")

hiveCtx = HiveContext(sc) rows = hiveCtx.sql("SELECT name, age FROM users")

Can also create from

- JDBC
- Cassandra
- Hbase
- Elastisearch
- JSON, CSV, sequence files, object files, various compressed formats.



## Ambari

* services -> spark -> Config -> Advanced spark-log4j-properties 

![4_003.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/4_Spark/4_003.png?raw=true)

![4_004.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/4_Spark/4_004.png?raw=true)

* log4j.rootCategory = INFO 를 ERROR로 변경 후 Save -> Restart

![4_005.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/4_Spark/4_005.png?raw=true)

* Spark2에도 동일하게 적용



### Putty 에서 실행해보기

* maria_dev 홈에서 ls 로  ml-100k  확인 후  (mkdir ml-100k) 

* 해당 폴더에 u.item, u.data파일 확인 (wget http://media.sundog-soft.com/hadoop/ml-100k/u.item )

* lecture 코드 다운로드 후 unzip

  wget http://media.sundog-soft.com/hadoop/Spark.zip

  unzip Spark.zip

* 코드 확인

  less LowestRatedPopularMovieSpark.py

* 코드 실행

  spark-submit LowestRatedPopularMovieSpark.py

* 결과

![4_007.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/4_Spark/4_007.png?raw=true)





## SparkSQL

Now as part of 2.0 they introduce a new concept called a data set as opposed to a data frame.

The lines between the two are very blurry in Python because Python's all dynamically typed.

But what you need to know is that a **data frame is really a data set of row objects** and **data set is a**

**more general term that can contain any sort of typed information not necessarily a row like you have in a data frame.**

So again this is just a way for Spark to actually get more information upfront about the structure of

your data and it can do that, to actually for example give you more compile time errors about problems instead of waiting until runtime.

That's kind of the real power of data sets.

And it also encourages you to use SQL queries within your scripts that actually allow further optimizations.

Again with Python it doesn't really mean you have to do anything differently necessarily but in Scala

Java that's more of a big deal.



DataFrame은 row object들의 set이다. 

Dataset은 모든 타입의 정보를 담을 수 있는 좀 더 일반적인 용어다. 데이터 프레임처럼 반드시 row일 필요는 없다. 다시 말하면 이것은 스파크가 좀 더 많은 데이터 구조에 대한 정보를 선행으로 얻기 위함이다. ( or 데이터 구조에 대한 선행 정보를 얻기 위함이다.)

예를들어 문제에 대해 런타임까지 기다리는 것 대신에  컴파일 타임 에러를 준다는 점이 데이터 셋의 힘!! 

또한, 더 나은 최적화를 위해 SQL 쿼리를 사용할 것을 권장한다. 파이썬에서는 크게 다를 것이 없지만, 스칼라나 자바에서는 중요하다.

![4_008.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/4_Spark/4_008.png?raw=true)

![4_009.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/4_Spark/4_009.png?raw=true)



#### [Activity]

1) Spark 버전 : export SPARK_MAJOR_VERSION=2

2) Script

```python
# Version 2
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def loadMovieNames():
    movieNames = {}
    with open("ml-100k/u.item") as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

def parseInput(line):
    fields = line.split()
    return Row(movieID = int(fields[1]), rating = float(fields[2]))

if __name__ == "__main__":
    # Create a SparkSession (the config bit is only for Windows!)
    spark = SparkSession.builder.appName("PopularMovies").getOrCreate()
    # .getOrCreatet will return a Spark session object
    

    # Load up our movie ID -> name dictionary
    movieNames = loadMovieNames()

    # Get the raw data
    lines = spark.sparkContext.textFile("hdfs:///user/maria_dev/ml-100k/u.data")
    # Convert it to a RDD of Row objects with (movieID, rating)
    movies = lines.map(parseInput)
    # Convert that to a DataFrame
    movieDataset = spark.createDataFrame(movies)

    # Compute average rating for each movieID
    averageRatings = movieDataset.groupBy("movieID").avg("rating")

    # Compute count of ratings for each movieID
    counts = movieDataset.groupBy("movieID").count()

    # Join the two together (We now have movieID, avg(rating), and count columns)
    averagesAndCounts = counts.join(averageRatings, "movieID")

    # Pull the top 10 results
    topTen = averagesAndCounts.orderBy("avg(rating)").take(10)

    # Print them out, converting movie ID's to names as we go.
    for movie in topTen:
        print (movieNames[movie[0]], movie[1], movie[2])

    # Stop the session
    spark.stop()

```



```python
from pyspark import SparkConf, SparkContext

# This function just creates a Python "dictionary" we can later
# use to convert movie ID's to movie names while printing out
# the final results.
def loadMovieNames():
    movieNames = {}
    with open("ml-100k/u.item") as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

# Take each line of u.data and convert it to (movieID, (rating, 1.0))
# This way we can then add up all the ratings for each movie, and
# the total number of ratings for each movie (which lets us compute the average)
def parseInput(line):
    fields = line.split()
    return (int(fields[1]), (float(fields[2]), 1.0))

if __name__ == "__main__":
    # The main script - create our SparkContext
    conf = SparkConf().setAppName("WorstMovies")
    sc = SparkContext(conf = conf)

    # Load up our movie ID -> movie name lookup table
    movieNames = loadMovieNames()

    # Load up the raw u.data file
    lines = sc.textFile("hdfs:///user/maria_dev/ml-100k/u.data")

    # Convert to (movieID, (rating, 1.0))
    movieRatings = lines.map(parseInput)

    # Reduce to (movieID, (sumOfRatings, totalRatings))
    ratingTotalsAndCount = movieRatings.reduceByKey(lambda movie1, movie2: ( movie1[0] + movie2[0], movie1[1] + movie2[1] ) )

    # Map to (rating, averageRating)
    averageRatings = ratingTotalsAndCount.mapValues(lambda totalAndCount : totalAndCount[0] / totalAndCount[1])

    # Sort by average rating
    sortedMovies = averageRatings.sortBy(lambda x: x[1])

    # Take the top 10 results
    results = sortedMovies.take(10)

    # Print them out:
    for result in results:

```





> 읽어보기 : [ 스파크(spark)버전에 따른 SparkConf와 SparkSession 사용하기](https://brocess.tistory.com/65)
>
> ```python
> // Spark 1.6
> val sparkConf = new SparkConf().setMaster("local[*]")
> sparkConf.set("spark.files", "file.txt")
>  
> // Spark 2.x
> val spark = SparkSession.builder.master("local[*]").getOrCreate()
> # sparksession.Builder.appName("PopularMovie")
> spark.conf.set("spark.files", "file.txt")
> 
> 
> # 출처: https://brocess.tistory.com/65 [행복한디벨로퍼]
> ```



* **.getOrCreate()**

These Spark scripts can actually recover, from themselves.

If you were to actually have some sort of a failure , 'get or create' means 

<u>1) I will either create a new Spark session</u> or

<u>2) if I didn't successfully stop from the last time, create from a saved snapshot of that session and pick up from what I left off.</u>





### MLLIB - Movie recommendations

- Machine learning Library



```
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql.functions import lit

# Load up movie ID -> movie name dictionary
def loadMovieNames():
    movieNames = {}
    with open("ml-100k/u.item") as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1].decode('ascii', 'ignore')
    return movieNames

# Convert u.data lines into (userID, movieID, rating) rows
def parseInput(line):
    fields = line.value.split()
    return Row(userID = int(fields[0]), movieID = int(fields[1]), rating = float(fields[2]))


if __name__ == "__main__":
    # Create a SparkSession (the config bit is only for Windows!)
    spark = SparkSession.builder.appName("MovieRecs").getOrCreate()

    # Load up our movie ID -> name dictionary
    movieNames = loadMovieNames()

    # Get the raw data
    lines = spark.read.text("hdfs:///user/maria_dev/ml-100k/u.data").rdd

    # Convert it to a RDD of Row objects with (userID, movieID, rating)
    ratingsRDD = lines.map(parseInput)

    # Convert to a DataFrame and cache it
    ratings = spark.createDataFrame(ratingsRDD).cache()

    # Create an ALS collaborative filtering model from the complete data set
    als = ALS(maxIter=5, regParam=0.01, userCol="userID", itemCol="movieID", ratingCol="rating")
    model = als.fit(ratings)

    # Print out ratings from user 0:
    print("\nRatings for user ID 0:")
    userRatings = ratings.filter("userID = 0")
    for rating in userRatings.collect():
        print movieNames[rating['movieID']], rating['rating']

    print("\nTop 20 recommendations:")
    # Find movies rated more than 100 times
    ratingCounts = ratings.groupBy("movieID").count().filter("count > 100")
    # Construct a "test" dataframe for user 0 with every movie rated more than 100 times
    popularMovies = ratingCounts.select("movieID").withColumn('userID', lit(0))

    # Run our model on that list of popular movies for user ID 0
    recommendations = model.transform(popularMovies)

    # Get the top 20 movies with the highest predicted rating for this user
    topRecommendations = recommendations.sort(recommendations.prediction.desc()).take(20)

    for recommendation in topRecommendations:
        print (movieNames[recommendation['movieID']], recommendation['prediction'])

    spark.stop()

```



#### Challenge

* Find the lowest-rated movies were polluted with movies only rated by one or two people

* Modify one or both of these scripts to only consider movies with at least ten ratings

  