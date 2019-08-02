**Amazon's Elastic MapReduce service**



- sets up a default spark configuration for you on top of hadoop's YARN cluster manager

  ( MapReduce and hadoop)



### 30. Setting up AWS/Elastic MapReduce Account and Setting UP Putty

#### 1. Getting Set up on EMR

m3.xlarge 4cpu 15 gb 0.266 per Hour

we're going to be doing a lot of work with EMR, the Elastic MapReduce product from Amazon Web Services

and it's not just MapReduce, it's actually a managed Hadoop framework so it spins up a Hadoop cluster

for you

and that actually includes Spark as well.



So click on the EC2 service here, EC2 is the last compute cloud which is the underlying service

that EMR uses to actually spin up the different computers in the cluster.





1.  EC2 -> key pair -> pem 다운로디
   * 주의 : 두 번은 못받으니까 반드시 잘 보관하기



2. puttygen.exe -> load -> .pem file -> save privatekey -> .ppk로 저장된다.
3. 이 키를 이용해서 cluster들을 관리할 수 있다.
4. putty -> configuration -> auth -> ppk file



====================

### 31. Partitioning

- Spark is not totally magic - you need to think about how your data is partitioned!
- 기존 코드를 그냥 돌리면 전혀 효과가 없다!
- join과 같은 큰 오퍼레이션을 하기 전에 .partitionBy() 를 RDD에 사용해야한다.
  - join(), cogroup(), groupWith(), Join(), groupByKey(), reduceByKey(), combineByKey(), lookup()
  - chunk로 나눈담에 executor에게 전달하면 executor 가 성공적으로 조절해준다.



#### 2. Choosing a partition size

- **Q**: How to determine the partition number mentioned in partitionBy , so the a pyspark job will perform better?

  **A**: There is no single answer to this question as it will always depend on the cluster size, availability and data nature.

  A general starting point is to assume each partition will be 200 MB and then calulate the number of partitions by dividing your full data size by 200



#### 3. Activity

* 달라진 것 

  * dataset  : 100k -> 1m

  * conf 비워두기 

    * we'll use the default that Elastic MapReduce sets up for us.

      And that will automatically tell Spark that it should be running on top of **EMR as Hadoop YARN cluster manager**, and that way you will automatically know **what the layout of the cluster is**, you know, **who's the master,** **how many client machines do I have**,

      **Who are they**, **How many executors do they have and what not**.

    

  * 구분자 :: 로 했음

  * param : **-executor-mamory 1g** filename.py 260

    * a default memory of 512 MB per executor -> 1GB
    * It means that's been broken up into 100 partitions for that join. 
    * other parameters that can use
      * -master yarn : YARN cluster에서 실행하고 싶을때 (but, EMR은 default로 설정해줌)





1. go to console
2. EMR -> create new cluster 

* [https://tech.cloud.nongshim.co.kr/2018/11/02/ec2-%EB%B2%94%EC%9A%A9-%EC%9D%B8%EC%8A%A4%ED%84%B4%EC%8A%A4-m4%EC%99%80-m5/](https://tech.cloud.nongshim.co.kr/2018/11/02/ec2-범용-인스턴스-m4와-m5/)



3. Use 10 instances for more reliable results.

4. Key pair : 이전에 만든 sparkey 사용 

5. ssh -> windows(putty) -> 4. in the host name field ... 값을 putty에 적용하여 접속! 

6. EMR 뜬다.

   

7. download :  aws s3 cp s3://sundog-spark/MovieSimilarities1M.py ./

8. ```
   download : aws s3 sp c3://sundog-spark/ml-1m/movies.dat ./
   ```

9. ```
   spark-submit --executor-memory 1g MovieSimilarities1M.py 260 -> Starwars 의 ID도 바뀜
   ```



10. 좋은 결과는 아님! strength가 60밖에 안되는데 위에 올라왔네.. -> try clean your data

11. TERMINATE ANY CLUSTERS in THE Elastic, in AWS concole using the EMR tab! 




##### Troubleshooting Spark on a Cluster

- default port is 4040 -> localhost:4040
- YARN에서 spark를 돌릴 경우 log들을 collect해야함.
- executor에게 할당된 메모리가 부족한 경우도 hang.






  