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