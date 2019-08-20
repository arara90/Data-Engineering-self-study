Section 2. Using Hadoop's core : HDFS and MapReduce



## HDFS





So like I said those blocks can be stored across several commodity computers and it doesn't just store

one copy of each block. In order to handle failure.





------- 위에는 다시 읽고 정리 ---

------- 밑에는 그림 ------

Let's say about how HDFS architecture works and a little bit more depth here so the way it works is there



* Name Node
* Data Node





#### Architecture 

##### Reading a File



##### Writing a File





Problem 1

It is important that **only one name node is active at a given time** otherwise clients might not agree on

where different blocks are stored and that would be bad.



solution 1

* the simplest way to do it is to backup your metadata constantly.

* So one configuration you might have is your name it might be writing out its edit logs **both** to its

  local disk and also to some NFS mount 

  that's talking to some backup data storage maybe even a different rack or even a different data center.

* And that way if your name node dies you can at least restore the log from that NFS backup. So when you bring up a new name node you can actually sort of bootstrap it using an edit log that you already had.