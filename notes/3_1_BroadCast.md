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



### 1. Caching RDD



## cache()

## persist()