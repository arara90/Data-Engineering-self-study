from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("SpendByCustomer")
sc = SparkContext(conf = conf)

######## aggregate() ##############


## EXAMPLE : 평균 구하기
sumCount = sc.parallelize([1, 2, 3, 4]).aggregate((0, 0)
                                                  , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                                                  , (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
avg = sumCount[0] / sumCount[1]
print('sumCount : ', sumCount, ' -> avg: ', avg)  # (10, 4)  -> avg:  2.5



## EXAMPLE 1 : '+' 와 '*'를 쓴다면?
sumCount5_2 = sc.parallelize([1, 2, 3, 4], 2).aggregate((1, 1)
                                                        , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                                                        , (lambda acc1, acc2: (acc1[0] * acc2[0], acc1[1] + acc2[1])))
print('sumCount5_2 : ', sumCount5_2)  # sumCount5_2 :  (32, 7)

# ** ** ** ** ** ** ** ** Sum 값만 확인 ** ** ** ** ** ** ** ** ** ** ** #
#
# sc.parallelize([1, 2, 3, 4], 2).aggregate((1, 1)
# ( 1+2+1(zero value)) * ((3+4)+1(zero value)) * 1(zero value) = 4 * 8 * 1 = 32

# sc.parallelize([1, 2, 3, 4], 2).aggregate((2, 1)
# ( 1+2+2(zero value)) * ((3+4)+2(zero value)) * 2(zero value) = 5 * 9 * 2 = 90

# sc.parallelize([1, 2, 3, 4], 2).aggregate((3, 1)
# ( 1+2 +3(zero value)) * ((3+4)+3(zero value)) * 3(zero value) = 6 * 10 * 3 = 180
#
# ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** #


## EXAMPLE 2 :  sc.parallelize([1,2,3,4],2) -> sc.parallelize([1,2,3,4], 1)
sumCount5_3 = sc.parallelize([1, 2, 3, 4], 1).aggregate((1, 1)
                                                        , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                                                        , (lambda acc1, acc2: (acc1[0] * acc2[0], acc1[1] + acc2[1])))
print('sumCount5_3 : ', sumCount5_3)  # sumCount5_3 :  (11, 6)
