# Other Spark Technologies and Libraries

### MLLIB (Machine learning Library)

* Special MLLIB DataTypes
  * Vector(Dense or sparse)
    * If you have a matrix in machine learning that where most of the cells are empty.
  * LabeledPoint
    * you can actually attach some sort of meaning to a dataset
  * Rating

* recommendation !! - 'Advanced Analytics with Spark'  by O'reilly

* ALS : Alternating Least Squares

  

# 실습

결과가 계속 다르다.

![](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/6_ASL_res1.png?raw=true)

![](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/6_ASL_res2.png?raw=true)



df.rando,Split([0.5,0.5])





## Streaming

- Analyzes continual streams of data
  - ex) processing log data from a website or server
- Data is aggregated and analyzed at some given interval
- can take data fed to some part, Amazon Kunesism, HDFS, Kafka, Flume, and others
- 'Checkingpointing' stores state to disk periodically for fault tolerance
- Python support for Spark Streaming is currently incomplete.*



* 'Windowed operations' can bombine results from multiple batches over some sliding time window

  * see window(), reduceByWindow(), reduceByKeyAndwindow()

* UpdateStateByKey()

  * Let's you maintain a state across many batches as time goes on
  * For example, running counts of some event

  

## GraphX

* vertexRDD - superheros
* EdgeRDD - a connection between two heros





================



data algorithm

MapReduce 

Data Mining - Statics for Dummies