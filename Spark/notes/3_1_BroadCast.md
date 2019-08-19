# Shared variables



## 1. BroadCast?







## 2. Accumulator

### * BFS * 

> ```
> Figure out the degrees of separation between any two superheroes in that data set.
> Find out how far apart Iron Man is to Spider Man 
> 
> 그림, 2degree
> ```





allows many executors to icrement a shared variable





# Item-based collaborative filtering in Spark

### Finding similar movies based on movie ratings

* prevent the need from recomputing it again.
* what's the difference between cache() and  persis()?
  - **persist()** optionally lets you **cache it to disk** instead of just memory, **just in case a node fails or something.** -> If you're really paranoid about losing that already, you don't want to lose it even of a node you can user persist() to make sure that wirtes it to disk. obviously that's going to take more time



## 1. Caching RDD

### cache(), persist() 

참고 : Learning Spark by O'reilly - p.189

* 단, cache()는 기본 스토리지 설정에서 persist()를 호출하는 것과 동일하다.

#### cache()

* **MEMORY_ONLY** 레벨로 메모리에 데이터를 저장한다. 즉 새로운 RDD 파티션을 저장할 메모리가 모자란다면 오래된 것들은 간단히 삭제될 수 있고, 나중에 삭제된 데이터가 다시 필요해지면 RDD는 재연산 된다.

#### persist()

* **MEMORY_AND_DISK** 레벨을 적용. 삭제 대신 RDD 파티션을 디스크에 내리게 되고 나중에 다시 필요해지면 간단하게 로컬 저장장치에서 메모리로 읽어 들일 수 있게 된다. 재연산 보다 비용도 적고 어느 정도 성능에 대한 예측도 가능해진다. 특히 재연산 비용이 매우 비싼 경우( ex. 데이터를 원격 DB에서 읽어온다거나)에 유용함.