from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("SpendByCustomer")
sc = SparkContext(conf = conf)

line = sc.parallelize(["hello world", "hi"])
words = line.flatMap(lambda line : line.split(" "))
words2 = line.map(lambda line : line.split(" "))
print("flatMap" , words.collect())  # flatMap ['hello', 'world', 'hi']
print("Map", words2.collect())      # Map [['hello', 'world'], ['hi']]

