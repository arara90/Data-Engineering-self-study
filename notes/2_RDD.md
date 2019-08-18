## RDD

### RDD의 기초

#### 1. RDD(Resilient Distributed Dataset)?

> **회복력(Resilient)**이 있다는의 뜻은? - 하둡 분산 시스템이 디스크 기반으로 데이터를
> 여러 개의 replication으로 카피한 후에, 데이터가 유실된 경우에 카피된 데이터를 복구
> 하는 데에 이용하는 방식으로 구성된 데 반해, 스파크는 메모리 기반으로서 데이터의 일
> 부가 유실되면 RDD를 만드는 방식을 기억하고 있다가 데이터를 처음부터 다시 만드는
> 방식으로 복구함.

* 단순하게 분산되어 있는 변경 불가능한 객체 모임(즉, 읽기 전용임!)

* RDD는 클러스터의 서로 다른 노드들에서 연산 가능하도록 여러개의 **파티션**으로 나뉜다.

* 사용자 정의 클래스를 포함해서 파이썬, 자바, 스칼라의 어떤 타입의 객체든 가질 수 있다.

  

#### 2. RDD 생성

* 외부 데이터 세트를 로드

```python
conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)
lines = sc.textFile("file:///data/ml-100k/u.data")
```

* 드라이버 프로그램에서 객체 컬력션(ex: list, set)을 분산 = **parallelize()**

```python
lines = sc.parallelize(["pandas", "i like pandas"])
```



#### 3. RDD의 두가지 연산 - Transformation / action

* **Transformation**

  * 존재하는 RDD에서 새로운 RDD를 생성 ex) Filtering

  * 각 RDD에 대해 가계도(Lineage graph)를 갖는다. 이 정보를 이용해 필요시 재연산 or 유실된 RDD 복구

    > ![lineage](https://postfiles.pstatic.net/MjAxNzExMTNfMjM0/MDAxNTEwNTUzNjgyMjk2.OMH9Heg5ydm9Q-IQwmmKllpjm6KUvsrhgVgN8_YikTUg.ZBidoCAz3ai20lLTQJwMz0i-3JtfOewbtN4w3vDKyRwg.JPEG.cafesky7/global-big-data-conference-sept-2014-aws-kinesis-spark-streaming-approximations-lambda-architecture-15-638.jpg?type=w2)
    >
    > 
    >
    > 이러한 RDD의 생성 순서를 Lineage라고 한다. Lineage는 DAG(Directed Acyclic Graph)의 형태를 가지는데, 이는 순환하지 않는 방향성 그래프이다. 이 곳에는 모든 RDD 생성 과정이 기록되어 있기 때문에 메모리에서 데이터가 유실되면 Lineage 기록에 따라 유실되었던 RDD를 생성할 수 있다.
    >
    > **[출처]** [Spark 바로 알기 RDD, Lineage, DAG, Lazy-Execution](https://blog.naver.com/cafesky7/221138921615)|**작성자** [고민없는 엔지니어](https://blog.naver.com/cafesky7)

* **action**

  * RDD를 기초로 결과 값을 계산하여 그 값을 드라이버 프로그램이나 외부 스토리지에 저장. 

    ex) first(), count(), collect()

    * **collect**()  : filter로 작은 크기의 RDD로 만든 후 분산 아닌 local에서 처리하고 싶을때 주로 사용

      즉, **collect() 사용 시**, **전체 데이터셋이 사용하는 단일 컴퓨터의 메모리에 올라올 수 있을 정도의 크기**여야하고, 너무 크면 사용할 수 없다. 

      

* **Lazy Evaluation**

  * 트랜스포메이션을 호출할 때 그 연산이 즉시 수행되지 않고, 스파크가 내부적으로 metadata에 이런 연산이 요청되었다는 사실만을 기록한다. 데이터 로드도 마찬가지.

  * 처음 Action을 사용하는 시점에서 처리한다.

    * 한번에 모든 트랜스포메이션 끼리의 연계를 파악하여 결과 도출에 필요한 Data만 합리적으로 연산

      ex) fist() : 처음 일치하는 라인이 나올때까지만 file을 읽고 전체 file을 읽지 않는다.

    * 연산들을 그룹화하여 Data 전달 횟수를 줄일 수 있다. 이것은 MapReduce(hadoop)에서는 항상 고민해야하는 과제이다.

* **Tip**! 

  * action과 transformation구분하기 위해서 **return타입** 확인. RDD면 Transformation 이외는 Action이다.

  

#### 4. RDD의 재사용(영속성) - persist() / cache()

* 스파크의 RDD들은 기본적으로 액션이 실행될 때마다 매번 새로 연산을 한다.

* **persist() **

  * **MEMORY_AND_DISK** 레벨을 적용 시, 삭제 대신 RDD 파티션을 디스크에 내리게 되고 나중에 다시 필요해지면 간단하게 로컬 저장장치에서 메모리로 읽어 들일 수 있게 된다. 재연산 보다 비용도 적고 어느 정도 성능에 대한 예측도 가능해진다. 특히 재연산 비용이 매우 비싼 경우( ex. 데이터를 원격 DB에서 읽어온다거나)에 유용함.

* **unpersist** () : 메모리에 많은 데이터를 올리려고 시도하면 스파크를 **LRU**(오래된 것을을 버리고 최근 것을 남기는 알고리즘)  캐시 정책에 따라 오래된 파티션들을 자동으로 버린다. -> 막상 필요한 데이터가 내려갈 수도 있음 -> RDD들은 unpersist()를 이용해서 직접 캐시에서 데이터를 삭제할 수 있다. 

  

* **cache()** 

  * **MEMORY_ONLY** 레벨, 메모리에 데이터를 저장한다. 즉 새로운 RDD 파티션을 저장할 메모리가 모자란다면 오래된 것들은 간단히 삭제될 수 있고, 나중에 삭제된 데이터가 다시 필요해지면 RDD는 재연산 된다.

  * 단, cache()는 기본 스토리지 설정에서 persist()를 호출하는 것과 동일하다

    
    
    

* **사용 예**

  1. RDD입력

  2. Filter 등을 이용해 새로운 RDD 생성

  3. persist() 사용하여 중간 결과 저장해둔다.

  4. counter, first()와 같은 액션 수행

참고 : Learning Spark by O'reilly - p.189



* **StorageLevel**
  * 데이터를 두 개의 머신에 복제하고 싶다면 각 레벨명 뒤에 '_2' 를 붙인다. ex) MEMORY_ONLY_2

![storagelevel](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/storagelevel.jpg?raw=tru)



### 많이 쓰이는 Transformation 과 Action

#### 1. 기본 RDD

##### Transformation

* **데이터 요소 위주 트랜스포메이션**

  * **map**()

    * 함수를 받아 RDD의 각 데이터에 적용하고 결과 RDD에 각 데이터의 새 결과값을 담는다.
    * 반환타입과 입력타입이 같지 않아도 된다.

  * **flatmap**()

    * 입력 데이터에 대해 여러 개의 아웃풋 데이터 생성 (즉 입력:결과 가 1:1로 매칭되지 않는 경우)
    
* 단일 값을 리턴하는 대신 반복자(iterator)를 리턴, 즉 반복자가 포함된 RDD를 리턴받는 것이 아니라 반복자가 생성하는 데이터들이 담긴 RDD를 받게된다. 즉 반환받은 반복자들을 **펼쳐놓는다(flatten)**고 생각하자. 
    
    
    
  ![mapvsflatmap](https://mblogthumb-phinf.pstatic.net/20160617_35/8x8x8x8x8x8_1466143661457FylV5_PNG/1.png?type=w2)
  
  * **filter**()
  
    
  
* **가상 집합 연산**

  * **distinct** : 단일 아이템인지 비교하기 위해 네트워크로 Data가 이리저리 전송(셔플링) 

    ​					=> 연산이 비싼 작업 

  * **union** : 중복 유지하며 합치는 작업

  * **intersection** : 여집합 / 중복제거 -> 셔플링 수반

  * **subtract** : 차집합

  * **cartesian** : 모든 가능한 쌍

    * 모든 사용자들에 대해 흥미있어 할 만한 제안을 파악
    * 가능한 쌍들에 대한 유사성 파악
    * 큰 사이즈에서 **비용이 매우 크다**

    

**{1,2,3,3}을 가지고 있는 RDD에 대한 RDD 트랜스포메이션**

| 함수 이름                                 | 용도                                                         | 예                        | 결과          |
| :---------------------------------------- | :----------------------------------------------------------- | :------------------------ | :------------ |
| map()                                     | RDD의 각 요소에 함수를 적용하고 결과 RDD를 되돌려준다.       | rdd.map(x -> x+1)         | {2,3,4,4}     |
| flatMap()                                 | RDD의 각 요소에 함수를 적용하고 반환된 반복자의 내용들로 이루어진 RDD를 되될려준다. 종종 단어 분해를 위해 쓰인다. | rdd.flatMap(x -> x.to(3)) | {1,2,3,2,3,3} |
| filter()                                  | filter()로 전달된 함수의 조건을 통과한 값으로만 이루어진 RDD를 되돌려 준다. | rdd.filter(x -> x != 1)   | {2,3,3}       |
| distinct()                                | 중복제거                                                     | rdd.distinct()            | {1,2,3}       |
| sample(withReplacement, fraction, [seed]) | 복원 추출(withReplacement-true)이나 비복원 추출로 RDD에서 표본을 뽑아낸다. | rdd.sample(false, 0.5)    | 생략          |



{1,2,3}과 {3,4,5}를 가진 두 RDD에 대한 트랜스포메이션**

| 함수 이름      | 용도                                                   | 예                      | 결과                         |
| :------------- | :----------------------------------------------------- | :---------------------- | :--------------------------- |
| union()        | 두 RDD에 잇는 데이터들을 합한 RDD를 생성한다.          | rdd.union(other)        | {1,2,3,3,4,5}                |
| intersection() | 양쪽 RDD에 모두 있는 데이터들만을 가진 RDD를 반환한다. | rdd.intersection(other) | {3}                          |
| subtract()     | 한 RDD가 가진 데이터를 다른 쪽에서 삭제한다            | rdd.subtract(other)     | {1,2}                        |
| cartesian()    | 두 RDD의 카테시안 곱                                   | rdd.cartesian(other)    | {{1,3},{1,4},{1,5} … ,{3,5}} |


 



##### Action

- **reduce**() : 두 개의 데이터를 합쳐 같은 타입 데이터 하나를 반환하는 함수를 받는다.

  - RDD의 총합, Count.. / sum = rdd.reduce(lambda x,y : x+y)

    ```python
    nums2 = sc.parallelize([1,2,3,4,5,6])
    sum2 = nums2.reduce(lambda x,y : x+y)
    print( 'Sum_reduce : ', sum2) 
    
    # ** ** ** ** ** ** result  ** ** ** ** ** ** ** 
    # Sum_reduce :  21
    ```

* **fold**() : reduce와 동일한 형태의 '함수'를 인자로 받으며, 추가로 각 파티션의 초기 호출에 쓰이는 'Zero Value'를 인자로 받는다.

  > Zero Value : 여러번 적용해도 바뀌지 않는값 = (수학에서) 멱등원(idempotent)
  >
  > ​	'+' 연산에서는 0,  '*' 연산에서는 1



* **reduce**() 와 fold()는 결과 type이 RDD내에서 연산하는 data 요소들과 동일해야 한다.
  * 평균 : rdd(elements) -- map---> rdd(element,1) -- reduce (sum연산) 을 거쳐야함.

-----------------------------------

* **aggreate**() : 동일한 타입으로 반환하지 않아도 된다. (reduce, fold와 다름)

  * Zero Value 필요

  * 두 개의 함수가 필요하다. 

    * [Aggregate설명] <https://whereami80.tistory.com/105>, <https://zzsza.github.io/data/2018/05/31/apache-spark-rdd-api/>

    1) 1번 함수 :  acc의 초기값으로 0이 설정, 여기에 지속적으로 + value

    2) 2번 함수 : 파티션의 결과들을 combine.  

  ```python
  ## EXAMPLE : 평균 구하기
  sumCount = sc.parallelize([1, 2, 3, 4]).aggregate((0, 0)
                                                    , (lambda acc, value: (acc[0] + value, acc[1] + 1)) #1번함수
                                                    , (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1]))) #2번함수
  avg = sumCount[0] / sumCount[1]  
  print(sumCount, ' -> avg: ', avg)   # (10, 4)  -> avg:  2.5
  
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
   
  ```

** **

* **collect**() 
  * 드라이버 프로그램에 값을 되돌려 주는 가장 간단하고 일반적으로 많이 쓰는 연산
  * 데이터가 **모두 드라이버 프로그램으로 COPY**되므로, **모든 데이터가 단일 컴퓨터의 메모리에 올라올 수 있어야한다는 제약**이 있다. 
* **take**(n) : 순서없이 n개의 데이터 값을 돌려준다.
  * 파티션 개수를 최소화하도록 동작하므로 특정 파티션의 값들만 되돌려 줄 수도 있다.
* **top**(n) : 순서가 정의되어 있다면, 상위의 값들만 뽑아온다.
* **takeSample**(withReplacement, num,seed) : 복원 혹은 비복원 추출로 **표본을 추출**

** **

* **foreach**() : 각 데이터에 대한 연산을 수행하지만 다시 로컬로 값을 전송하지 않는다.

  * JSON을 만들어서 웹 서버에 전송하거나, DB에 값을 저장할 때 쓸 수 있다.

  

**{1,2,3,3}을 갖고 있는 RDD에 대한 기본 액션**

| 함수 이름                                | 용도                                      | 예                                                           | 결과                |
| :--------------------------------------- | :---------------------------------------- | :----------------------------------------------------------- | :------------------ |
| collect()                                | RDD의 모든 데이터요소 리턴                | rdd.collect()                                                | {1,2,3,3}           |
| count()                                  | RDD의 요소 개수 리턴                      | rdd.count()                                                  | 4                   |
| countByValue()                           | RDD에 있는 각 값의 개수 리턴              | rdd.countByValue()                                           | {{1,1},{2,1},{3,2}} |
| take(num)                                | RDD의 값들 중 num개 리턴                  | rdd.take(2)                                                  | {1,2}               |
| top(num)                                 | RDD의 값들 중 상위 num개 리턴             | rdd.top(2)                                                   | {3,3}               |
| takeOrdered(num(ordering)                | 제공된 ordering 기준으로 num개 값 리턴    | rdd.takeOrdered(2)(myOrdering)                               | {3,3}               |
| takeSample(withReplacement, num, [seed]) | 무작위 값을 리턴                          | rdd.takeSample(false,1)                                      | 생략                |
| reduce(func)                             | RDD의 값들을 병렬로 병합 연산한다.        | rdd.reduce((x,y) -> x+y)                                     | 9                   |
| fold(zero)(func)                         | reduce()와 동일하나 제로 밸류를 넣어준다. | rdd.fold(0)(x,y) -> x+y                                      | 9                   |
| aggregate(zeroValue)(seqOP, combOp)      | reduce()와 유사하나 다른 타입을 리턴한다. | rdd.aggregate((0,0))((x,y) -> (x._1 + y, x._2 +1), (x,y) -> (x._1 + y._1, x._2 + y._2)) | {9,4}               |
| foreach(func)                            | RDD의 각값에 func을 적용한다.             | rdd.foreach(func)                                            | 없음                |



#### 영속화

[ 더 읽을 거리 : <https://ourcstory.tistory.com/149> ]

* 영속화 요청 : RDD를 계산한 노드들은 그 파티션들을 저장한다.

  해당 노드에 장애가 생기면 스파크는 필요 시 유실된 데이터 파티션을 재연산한다.

  지연없이 노드 장애에 대응하고 싶다면 **데이터를 복제하는 정책**을 선택할 수 있다.

  

* 스파크는 목적에 맞는 여러 수준의 영속화를 제공한다. 스칼라와 자바에서는 기본적으로 persist()가 데이터를 JVM 힙(heap)에 직렬화되지 않은 객체 형태로 저장한다. **파이썬에서 영속화된 데이터는 늘 직렬화해야 하므로 기본적으로는 JVM 힙에 피클된(파이썬의 직렬화) 객체가 저장된다**. 데이터를 디스크나 오프힙(off-heap) 저장 공간에 쓸 때는 데이터가 늘 직렬화된다.

  

> # **직렬화**? 
>
> <http://woowabros.github.io/experience/2017/10/17/java-serialize.html>
>
> ### 자바 직렬화가 무엇(what)인가요??
>
> - 자바 직렬화란 자바 시스템 내부에서 사용되는 객체 또는 데이터를 외부의 자바 시스템에서도 사용할 수 있도록 **바이트(byte) 형태로 데이터 변환하는 기술**과 바이트로 변환된 데이터를 다시 객체로 변환하는 기술(역직렬화)을 아울러서 이야기합니다.
>
> - 시스템적으로 이야기하자면 JVM(Java Virtual Machine 이하 JVM)의 **메모리에 상주(힙 또는 스택)되어 있는 객체 데이터를 바이트 형태로 변환하는 기술**과 직렬화된 바이트 형태의 데이터를 객체로 변환해서 JVM으로 상주시키는 형태를 같이 이야기합니다.
>
>   
>
> ### [python] serialize (직렬화)
>
> <https://itholic.github.io/python-serialize/>
>
> * 즉, 직렬화란 “스트림 전송을 위해 **일정한 규칙**에 의해 데이터를 일련의 바이트로 변형하는 작업” 
> * pickle, JSON같은 개념들이 바로 그 “일정한 규칙”들 중 하나이다.
>
> * pickle 예제 확인



* [persist(), cache()](# 4. RDD의 재사용(영속성) - persist() / cache())

 

