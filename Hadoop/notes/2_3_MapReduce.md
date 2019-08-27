But basically mappers are what transform your data and reducers are what aggregates your data.



MapReduce also provides a mechanism for handling failure.

shuffle and sort will put together all the given movies for each unique user and sort those users for

us so we end up with this from this example where we just have a list of user IDs associated with the

list of keys associated with the list of movie IDs associated with each user ID and are

reduced can then process each incoming list of values each an incoming list of movies.





### How MapReduce distributes processing

You know you kick things off from a client node 

there's a **Resource manager** that's **keeping track of all the different computers and what has availability.**

And then you have **an Application master** responsible for **keeping an eye on all of your tasks** 

and **these Node managers** are **keeping an eye on the individual PCs as a whole**.





One other thing worth talking about is that when your resource manager decides where to actually

launch a given mapper or a given reducer it will try to actually make that run as close to the data as

possible.

So it's going to try to make sure that a map responsible for processing a given subset of your input

data will actually be running on the same machine that contains a copy of those blocks that it needs

whenever possible.

And if that's not possible it will try to make sure it's as close to it in the network as possible.

So it does a lot of work to make sure that you're not sending stuff over the network when you don't

have to.





### How are mappers and reducers written?



### Handling Failure

1. The downside of using big clusters of commodity PCs or commodity hardware is that since they're a commodity : 상품 PC를 쓰는 단점

   they tend to **go down at times** and you need to deal with that. * at times : 가끔, 때때로



> Hot Standby  : 상시 대기 방식
>
> * 내용 교체 프로그램이나 데이터를 언제라도 꺼낼 수 있는 상태로 컴퓨터를 대기 시켜 놓고, 현재 사용중인 컴퓨터에 고장이 발생하면 바로 전환시킬 수 있는 시스템. 
>
>   보통 2대 이상의 컴퓨터를 갖추고 있어 고장 발생시 즉시 다른 컴퓨터로 대체하여 중단 없이 일을 처리한다.
>
> Cold Standby : 수동 예비 방식
>
> * 이중화 [시스템](https://terms.naver.com/entry.nhn?docId=853283&ref=y)에서 현재 사용하고 있는 시스템에 장애가 발생했을 때, 운용자가 예비 시스템의 전원을 넣어 초기 [프로그램](https://terms.naver.com/entry.nhn?docId=833746&ref=y) 처리를 진행하면서 현재 사용 중인 시스템의 운용을 계속하는 방식.



Real Example - How many of each rating type exist?

```python
def mapper_get_ratings(self, _, line):
(userID, movieID, rating timestamp) = line.split('\t')
yield rating, 1
```

yield means this is what our mapper is going to give up, when it goes back to the mapreduce framework.

> **[yield]**
>
>   <https://kkamikoon.tistory.com/90>
>
> Generator는 Iterator를 생성해주는 함수라고 간단하게 설명할 수 있겠습니다. iterator는 next()함수를 통해 순차적으로 값을 가져오는 object를 말합니다.  
>
> Yield는 값을 return 하고 다시 함수로 돌아가게끔해주는 것입니다. (두번째 그림)
>
> ![](https://t1.daumcdn.net/cfile/tistory/244BA249588A1BB612)
>
> ![](https://t1.daumcdn.net/cfile/tistory/2764364B588A1CB325)
>
> 출처: <https://kkamikoon.tistory.com/90> [컴퓨터를 다루다]  



```python
def recuder_count_ratings(self, key, value):
	yield key, sum(value)
```



```python
def mapper_get_ratings(self, _, line):
	(userID, movieID, rating timestamp) = line.split('\t')
yield rating, 1

def recuder_count_ratings(self, key, value):
	yield key, sum(value)
```

