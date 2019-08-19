from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MinTemperatures")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    stationID = fields[0]
    entryType = fields[2]
    temperature = float(fields[3]) * 0.1 * (9.0 / 5.0) + 32.0
    return (stationID, entryType, temperature)

lines = sc.textFile("file:///TamingBigdataWithSparkAndPython/data//1800.csv")

# ID, Date, entryType, Temperture or precipitation  --(parseLine)--> ID, entryType ,Temperture
parsedLines = lines.map(parseLine)

# TMIN인 Line만 필터링
minTemps = parsedLines.filter(lambda x: "TMIN" in x[1])

# ID와 Temperture만
stationTemps = minTemps.map(lambda x: (x[0], x[2]))
# print(stationTemps.collect())

# Key값(ID)을 기준으로 최저값을 찾음
minTemps = stationTemps.reduceByKey(lambda x, y: min(x,y))
results = minTemps.collect();

for result in results:
    print(result[0] + "\t{:.2f}F".format(result[1]))
