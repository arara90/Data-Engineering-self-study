# diplay movie names, not ID's

# !! broadcast variables !!
# https://opennote46.tistory.com/236
# Spark offers a way to actually just transfer information once to every excutor node in your SPARK
# so you can actually transmit information to every node on your cluster and do that efficiently.
# .broadcast() , value()
# ! broadcast 최적화? https://tomining.tistory.com/86
# 큰 데이터를 broadcast할 때, data serializations을 잘 선택하는 것이 중요하다.
# 그 이유는 network를 통해 Broadcast데이터를 각 worker에 보내는 시간이 병목될 수 있기 때문이다.


# input data :
# # 1. Marvel-graph.txxt
# # Every Line has the first century being a given hero fall by a list of all the other heroes that they appeared with#
# # given-hero hero1 hero2 hero3...

# # 2. Marvel-names.txt
# # superheroID, name

from pyspark import SparkConf, SparkContext

def loadMovieNames():
    movieNames = {} # dictionary
    with open("C://TamingBigdataWithSparkAndPython/data/ml-100k/u.ITEM", encoding='ISO-8859-1') as f:
        for line in f:
            fields = line.split('|')
            movieNames[int(fields[0])] = fields[1]
    return movieNames

conf = SparkConf().setMaster("local").setAppName("PopularMovies")
sc = SparkContext(conf = conf)

# broadcast that to everynode of our cluster so that it's available when needed
nameDict = sc.broadcast(loadMovieNames())

lines = sc.textFile("file:///TamingBigdataWithSparkAndPython/data/ml-100k/u.data")
movies = lines.map(lambda x: (int(x.split()[1]), 1))
movieCounts = movies.reduceByKey(lambda x, y: x + y)

flipped = movieCounts.map( lambda x : (x[1], x[0]))
sortedMovies = flipped.sortByKey()

# nameDict에서 매칭되는 movieID를 찾아서 value를 가지고 온다. 즉, (movieName, countMovie)의 결과
# 만약 위에서 u.item을 broadcast해주지 않으면 매 dict마다 across the wire 할거야.
sortedMoviesWithNames = sortedMovies.map(lambda countMovie : (nameDict.value[countMovie[1]], countMovie[0]))
# lambda (count,movie) : (nameDict.value[movie], count))
# lambda (x,y) : (nameDict.value[y], x))

results = sortedMoviesWithNames.collect()

for result in results:
    print (result)
