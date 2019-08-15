from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("SpendByCustomer")
sc = SparkContext(conf = conf)

######## aggregate() ##############

#############################  + +
sumCount1 = sc.parallelize([1,2,3,4],1).aggregate((0,0)
                          , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
print('sumCount1 : ',sumCount1[0]) # 10

sumCount2 = sc.parallelize([1,2,3,4],2).aggregate((0,0)
                          , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
print('sumCount2 : ',sumCount2[0]) # 10


#############################  * *
sumCount3 = sc.parallelize([1,2,3,4],1).aggregate((1,1)
                          , (lambda acc, value: (acc[0] * value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] * acc2[0], acc1[1] + acc2[1])))
print('sumCount3 : ',sumCount3[0]) # 24


sumCount = sc.parallelize([1,2,3,4],2).aggregate((1,1)
                          , (lambda acc, value: (acc[0] * value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] * acc2[0], acc1[1] + acc2[1])))
print('sumCount : ',sumCount[0]) # 24



#############################  + *
sumCount4 = sc.parallelize([1,2,3,4],1).aggregate((0,1)
                          , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] * acc2[0], acc1[1] + acc2[1])))
print('sumCount4 : ',sumCount4[0]) #0

## ★★★
sumCount5_2 = sc.parallelize([1,2,3,4],2).aggregate((1,1)
                          , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] * acc2[0], acc1[1] + acc2[1])))
print('sumCount5_2 : ',sumCount5_2[0]) # 32
# aggregate((1,1) -> ( 1+2 + 1(zero value)) * ( (3+4)  + 1(zero value) ) * 1( zero value)  = 4 * 8 * 1 = 32
# aggregate((2,1) -> ( 1+2 + 2(zero value)) * ( (3+4)  + 2(zero value) ) * 2( zero value)  = 5 * 9 * 2 = 90
# aggregate((3,1) -> ( 1+2 + 3(zero value)) * ( (3+4)  + 3(zero value) ) * 3( zero value)  = 6 * 10 * 3 = 180

sumCount5 = sc.parallelize([1,2,3,4],2).aggregate((0,1)
                          , (lambda acc, value: (acc[0] + value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] * acc2[0], acc1[1] + acc2[1])))
print('sumCount5 : ',sumCount5[0]) # 0


#############################  * +
sumCount6 = sc.parallelize([1,2,3,4],1).aggregate((1,0)
                          , (lambda acc, value: (acc[0] * value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
print('sumCount6 : ', sumCount6[0]) # 25


sumCount7 = sc.parallelize([1,2,3,4],2).aggregate((1,0)
                          , (lambda acc, value: (acc[0] * value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
print('sumCount7 : ', sumCount7[0]) # 15

sumCount8 = sc.parallelize([1,2,3,4],2).aggregate((2,0)
                          , (lambda acc, value: (acc[0] * value, acc[1] + 1))
                          , (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
print('sumCount8 : ', sumCount7[0]) # 15

