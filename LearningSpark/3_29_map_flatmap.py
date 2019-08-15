from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("SpendByCustomer")
sc = SparkContext(conf = conf)

line = sc.parallelize(["hello world", "hi"])
words = line.flatMap(lambda line : line.split(" "))
words2 = line.map(lambda line : line.split(" "))
print("flatMap" , words.collect())  # flatMap ['hello', 'world', 'hi']
print("Map", words2.collect())      # Map [['hello', 'world'], ['hi']]

nums = sc.parallelize([1,2,3,4,5,6])
sum = nums.map(lambda x : x+x).collect()
print( 'Sum: ', sum)                    # Sum:  [2, 4, 6, 8, 10, 12]

nums1 = sc.parallelize([1,2,3,4,5,6])
sum1 = nums1.flatMap(lambda x : x+x)           # PythonRDD[6] at RDD at PythonRDD.scala:52
print( 'Sum_flatmap : ', sum1)

sum_to1 = nums1.flatMap(lambda x : x.to(3))    # PythonRDD[6] at RDD at PythonRDD.scala:52 / .collect()붙이면 type error
print( 'sum_to1 : ', sum_to1)

sum_to2 =nums.flatMap(lambda x: [x,x,x]).collect()
print( 'sum_to2 : ', sum_to2)

sum_to3 =nums.flatMap(lambda x: [x,x,x]).collect()
print( 'sum_to3 : ', sum_to3)

nums2 = sc.parallelize([1,2,3,4,5,6])
sum2 = nums2.reduce(lambda x,y : x+y)
print( 'Sum_reduce : ', sum2)

