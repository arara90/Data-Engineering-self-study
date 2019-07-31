from pyspark import SparkConf, SparkContext

# map() -> one to one
# flatmap() -> one to any

conf = SparkConf().setMaster("local").setAppName("WordCount")
sc = SparkContext(conf = conf)

input = sc.textFile("file:///TamingBigdataWithSparkAndPython/data/book.txt")
words = input.flatMap(lambda x: x.split()) # 하나의 독립된 row로 만들어줌
wordCounts = words.countByValue()

for word, count in wordCounts.items():
    # take care of some encoding issues :
    # In case something was encoded as utf8 or unicode in original text
    # display it by converting it to ascii formats
    cleanWord = word.encode('ascii', 'ignore')
    if (cleanWord):
        print(cleanWord.decode() + " " + str(count))

# Post, Car?, good,) 와 같이 clean하지 않은 결과를 보여준다.