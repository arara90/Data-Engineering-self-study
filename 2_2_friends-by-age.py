from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("FriendsByAge")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    age = int(fields[2])
    numFriends = int(fields[3])
    return (age, numFriends)

lines = sc.textFile("file:///TamingBigdataWithSparkAndPython/data/fakefriends.csv")
rdd = lines.map(parseLine)

# reduceByKey : https://www.ridicorp.com/blog/2018/10/04/spark-rdd-groupby/
totalsByAge = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])

print(totalsByAge) # PythonRDD[6] at RDD at PythonRDD.scala:52
print(type(totalsByAge.collect())) #<class 'list'> -> 즉, collect는 각 언어에 맞는 배열형태로 전환해준다. 여기서는 list

# results = totalsByAge.collect()
# for result in results:
#     print(result)

results2 = averagesByAge.collect()
for result in results2:
    print(result)
