import re
from pyspark import SparkConf, SparkContext

def normalizeWords(text):
    return re.compile(r'\W+', re.UNICODE).split(text.lower())

conf = SparkConf().setMaster("local").setAppName("WordCount")
sc = SparkContext(conf = conf)

input = sc.textFile("file:///TamingBigdataWithSparkAndPython/data/book.txt")
words = input.flatMap(normalizeWords)

# how many times the word occurs
# transform every word into a key,value pair of the word and the number 1
wordCounts = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
# flip
wordCountsSorted = wordCounts.map(lambda x: (x[1], x[0])).sortByKey()
#wordCountsSorted = wordCounts.map(lambda (x,y): (y, x)).sortByKey()
results = wordCountsSorted.collect()

# for result in results:
#     count = str(result[0])
#     word = result[1].encode('ascii', 'ignore')
#     if (word):
#         print(word.decode() + ":\t\t" + count)
