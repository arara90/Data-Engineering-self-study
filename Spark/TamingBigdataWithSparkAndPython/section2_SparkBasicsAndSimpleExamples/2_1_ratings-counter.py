from pyspark import SparkConf, SparkContext
import collections

# conf에서 cluster or local 정할 수 있음
# local machine을 masterNode로 지정했음
# We're gonna runspar it in a single thread on a single process that's what local means
conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)

# 1. "file:/// 만나면 local , hdfs:///만나면 hdfs 사용"
#. 2. .data file??
# lines = sc.textFile("file:///C:/SparkCourse/ml-100k/u.data")
lines = sc.textFile("file:///TamingBigdataWithSparkAndPython/data/ml-100k/u.data")
# userID movieID ratings date

ratings = lines.map(lambda x: x.split()[2])

# 평점을 기준으로 counting
result = ratings.countByValue()
print(result)               # defaultdict(<class 'int'>, {'3': 27145, '1': 6110, '2': 11370, '4': 34174, '5': 21201})
print(result.items())       # dict_items([('3', 27145), ('1', 6110), ('2', 11370), ('4', 34174), ('5', 21201)])

# sorted(dict.items())하면 키값으로 정렬한다. (value값이 아님)
a = sorted(result.items())
print(type(a),type(a[0]), a)                    # list, tuple, [('1', 6110), ('2', 11370), ('3', 27145), ('4', 34174), ('5', 21201)]
# tuple? 요소를 삭제하거나 변경할 수 없다.

# 그런데 왜 또 OrderedDict를 하는거징? -> 순서가 있는 Dict로 저장한다.
sortedResults = collections.OrderedDict(a)
print(type(sortedResults), sortedResults)        # OrderedDict([('1', 6110), ('2', 11370), ('3', 27145), ('4', 34174), ('5', 21201)])
for key, value in sortedResults.items():
    print("%s %i" % (key, value))
