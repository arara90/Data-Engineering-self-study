from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster('local').setAppName('totalAmount')
sc = SparkContext(conf=conf)
input = sc.textFile('file:///TamingBigdataWithSparkAndPython/data/customer-orders.csv')

def parseLine(line):
    # 1. split
    values = line.split(',')
    return (int(values[0]), float(values[2]))

parseLines = input.map(parseLine)
totalAmount = parseLines.reduceByKey(lambda x,y : x + y)
result = totalAmount.sortByKey().collect()

for item in result:
    print(str(item[0]) + "\t{:.2f}".format(item[1]))

########################## instructor example ##########################
# from pyspark import SparkConf, SparkContext
#
# conf = SparkConf().setMaster("local").setAppName("SpendByCustomer")
# sc = SparkContext(conf = conf)
#
# def extractCustomerPricePairs(line):
#     fields = line.split(',')
#     return (int(fields[0]), float(fields[2]))
#
# input = sc.textFile("file:///sparkcourse/customer-orders.csv")
#
# mappedInput = input.map(extractCustomerPricePairs)
#
# totalByCustomer = mappedInput.reduceByKey(lambda x, y: x + y)
#
# results = totalByCustomer.collect();
#
# for result in results:
#     print(result)
#
# ############### instructor example _ sort #######################3
# from pyspark import SparkConf, SparkContext
#
# conf = SparkConf().setMaster("local").setAppName("SpendByCustomerSorted")
# sc = SparkContext(conf = conf)
#
# def extractCustomerPricePairs(line):
#     fields = line.split(',')
#     return (int(fields[0]), float(fields[2]))
#
# input = sc.textFile("file:///sparkcourse/customer-orders.csv")
#
# mappedInput = input.map(extractCustomerPricePairs)
#
# totalByCustomer = mappedInput.reduceByKey(lambda x, y: x + y)
#
# flipped = totalByCustomer.map(lambda x: (x[1], x[0]))
#
# totalByCustomerSorted = flipped.sortByKey()
#
# results = totalByCustomerSorted.collect();
#
# for result in results:
#     print(result)
