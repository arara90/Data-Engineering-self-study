Section 2. Using Hadoop's core : HDFS and MapReduce



# HDFS

* 실시간보다는 배치처리를 위해 설계되어 빠른 데이터 응답시간이 필요한 작업에 적합하지 않다.

* 네임노드가 단일 실패 지점(SPOF) -> 네임노드 관리 중요

  

### 특징

#### 블록단위저장

-  블록사이즈보다 **작은 파일**은 **기존 파일의 사이즈**로 저장

- ,블록 사이즈보다 **큰 파일**은  데이터파일은 **블록단위 나누어** 저장

  

#### 블록복제를 이용한 장애복구

* HDFS는 장애 복구를 위해서 각 블록을 복제하여 저장 (  블록의 기본 복제 단위 : 3 , 1GB 저장 -> 3GB 필요)
* 하나의 블록은 3개의 블록으로 복제되고, **같은 랙(Rack)의 서버**와 **다른 랙(Rack)의 서버로 복제**되어 저장
* 블록에 문제가 생기면 복제한 다른 블록을 이용해서 데이터를 복구.
* So like I said those blocks can be stored across several commodity computers and it doesn't just store one copy of each block. In order to handle failure.

#### 읽기 중심

* 데이터를 한 번 쓰면 여러 번 읽는 것을 목적

* 파일의 수정을 제한하여 동작을 단순화하고 이를 통해 데이터를 읽을 때 속도를 높임

  

#### 데이터 지역성

* **맵리듀스는** HDFS의 데이터 지역성을 이용해서 처리 속도를 증가
* 데이터가 있는 곳에서 알고리즘을 처리하여 네트워크를 통해 대용량 데이터를 이동시키는 비용을 줄임.



## Name Node 

#### 메타 데이터 관리

* 메타데이터 

  * 파일이름, 파일크기, 생성시간, 접근권한, 소유자 및 그룹 소유자, 파일이 위치한 블록의 정보 등

  *  사용자가 설정한 위치(dfs.name.dir)에 보관

  * 네임노드가 **실행 될 때 파일을 읽어서 메모리에 보관**

  * 운영중에 발생한 수정사항은 네임노드의 메모리에는 바로 적용되고, 데이터의 수정사항을 다음 구동시 적용을 위해서 주기적으로 Edits 파일로 저장합니다.

    

*  fsimage 파일(네임스페이스, 블록 정보) 

* edits 파일(트랜잭션로그 - 파일 생성, 삭제 / 메모리에 저장하다가 주기적으로 생성)

* 각 데이터노드에서 전달하는 메타데이터를 받아서 전체 노드의 메타데이터 정보와 파일 정보를 묶어서 관리



#### 데이터 노드의 관리

* 네임노드는 데이터노드가 주기적으로 전달하는 **하트비트**(3초, dfs.heartbeat.interval)와 **블록리포트**(6시간, dfs.blockreport.intervalMsec)를 이용하여 데이터 노드의 동작상태, 블록상태를 관리
  * **하트비트**가 도착하지 않으면 네임노드는 데이터노드가 동작 하지 않는 것으로 간주하고, 더이상 IO 가 발생하지 않도록 조치
  * **블록리포트**를 이용하여 HDFS에 **저장된 파일에 대한 최신 정보를 유지**합니다. 블록리포트에는 데이터노드에 저장된 블록 목록과 각 볼록이 로컬 디스크의 어디에 저장되어 있는지에 대한 정보를 가지고 있습니다.



## Data Node 

#### 파일 저장

#### 네임노드 구동 과정

* fsimage와 edits를 읽거 작업을 처리하기 때문에 두 파일의 크기가 크면 구동 시작시간이 오래 걸린다.

  > Fsimage를 읽어 메모리에 적재합니다.
  >
  > Edits 파일을 읽어와서 변경내역을 반영
  >
  > 현재의 메모리 상태를 스냅샷으로 생성하여 Fsimage 파일 생성
  >
  > 데이터 노드로부터 블록리포트를 수신하여 매핑정보 생성서비스 시작

  

## Block

#### 블록스캐너

데이터 노드는 주기적으로 블록 스캐너를 실행하여 블록의 체크섬을 확인하고 오류가 발생하면 수정합니다.

#### 블록 캐싱

데이터 노드에 저장된 데이터 중 자주 읽는 블록은 블록 캐시(block cache)라는 **데이터 노드의 메모리에 명시적으로 캐싱**할 수 있습니다. 파일 단위로 캐싱 할 수도 있어서 조인에 사용되는 데이터들을 등록하여 읽기 성능을 높일 수 있습니다.

```
$ hdfs cacheadmin
Usage: bin/hdfs cacheadmin [COMMAND]
          [-addDirective -path <path> -pool <pool-name> [-force] [-replication <replication>] [-ttl <time-to-live>]]
          [-modifyDirective -id <id> [-path <path>] [-force] [-replication <replication>] [-pool <pool-name>] [-ttl <time-to-live>]]
          [-listDirectives [-stats] [-path <path>] [-pool <pool>] [-id <id>]
          [-removeDirective <id>]
          [-removeDirectives -path <path>]
          [-addPool <name> [-owner <owner>] [-group <group>] [-mode <mode>] [-limit <limit>] [-maxTtl <maxTtl>]
          [-modifyPool <name> [-owner <owner>] [-group <group>] [-mode <mode>] [-limit <limit>] [-maxTtl <maxTtl>]]
          [-removePool <name>]
          [-listPools [-stats] [<name>]]
          [-help <command-name>]

# pool 등록 
$ hdfs cacheadmin -addPool pool1
Successfully added cache pool pool1.

# path 등록
$ hdfs cacheadmin -addDirective -path /user/hadoop/shs -pool pool1
Added cache directive 1

# 캐쉬 확인 
 hdfs cacheadmin -listDirectives
Found 1 entry
 ID POOL    REPL EXPIRY  PATH             
  1 pool1      1 never   /user/hadoop/shs 
```









------- 위에는 다시 읽고 정리 ---

------- 밑에는 그림 ------

Let's say about how HDFS architecture works and a little bit more depth here so the way it works is there



## Architecture 

##### Reading a File



##### Writing a File





## Namenode Resilience

> 참고 1  : <https://brocess.tistory.com/190>

### backup metadata constantly

* 네임노드는 파일시스템 트리와 그 트리에 포함된 모든 파일과 디렉터리에 대한 메타 데이터를 유지.

* 이 정보는 namespace image와 edit log라는 두 종류의 파일로 로컬 디스크에 영속적으로 저장.

* 블록의 **위치 정보는 시스템 시작시에 모든 데이터 노드로부터 받아서 재구성**하기 때문데 디스크에 저장하지는 않는다.

* Write out edit logs **both** to its **local disk** and also to some **NFS mount** 

* That's talking to some backup data storage maybe even a different rack or even a different data center.

  

### **Secondary Namenode**( 보조 네임노드 )

보조 네임노드의 주 역할은 에디트 로그가 너무 커지지 않도록 주기적으로 **네임스페이스 이미지를 에디트 로그와 병합하여 새로운 네임스페이스 이미지를 만드는 것**이다. (파일을 머지하면서 Edits 파일을 삭제하기 때문에 디스크 부족 문제도 해결 )

  병합 작업을 수행하기 위해 보조 네임노드는 충분한 CPU와 네임노드와 비슷한 용량의 메모리가 필요하므로 별도의 물리 머신에서 실행되는 것이 좋다. 

  또한 보조 네임노드는 주 네임노드에 장애가 발생할 것을 대비해서 네임스페이스 이미지의 복제본을 보관하는 역할도 맡는다.

  하지만 주 네임노드의 네임스페이스 이미지는 약간의 시간차를 두고 보조 네임노드로 복제되기 때문에 주 네임노드에 장애가 발생하면 어느 정도의 데이터 손실은 불가피하다.

  이럴 때 일반적인 복구 방식은 **NFS에 저장된 주 네임노드의 메타데이터 파일**을 **보조 네임노드로 복사하여 새로 병합된 네임스페이스 이미지를 만들고 그것을 새로운 주 네임노드에 복사한 다음 실행**하는 것이다.

출처: <https://brocess.tistory.com/190> [행복한디벨로퍼]  



* All it's doing is **maintaining a merged copy of the edit log from your primary name node**.

  So it's not really a name node per se(네임노드 그 차제),  it's just maintaining a copy at all times of that edit log.

* So this is a little bit better than the previous situation where if you do need to restore from a failed name node. you can do so from an edit log **that has a more up to date copy from your secondary name node** and spin that up on your secondary name node.

  

### HDFS Federation

*  **디렉토리(네임스페이스) 단위로 네임노드를 등록하여 사용하는 것**. 

  즉, 하나의 클러스터에 여러 name node를 사용할 수 있도록 한것 

> 참고 1 : https://xlos.tistory.com/1555
>
> 참고 2 : https://wikidocs.net/23624



- **네임스페이스**(디렉토리의 정보)와 **블록 풀**(블록의 정보)을 **각 네임노드가 독립적으로 관리**합니다.  

- **네임스페이스 볼륨**(네임스페이스와 블록풀)은 독립적으로 관리되기 때문에 하나의 네임노드에 문제가 생겨도 다른 네임노드에 영향을 주지 않는다.

![hdfs federation](https://hadoop.apache.org/docs/r2.7.2/hadoop-project-dist/hadoop-hdfs/images/federation.gif)



* This isn't really about reliability so much as the **ability to scale beyond a single name node**.

  - 하나의 Cluster내에서 여러 name node를 사용할 수 있도록 한 것.

  So remember we said that HD with us is really optimized for large files and **not so much for lots and lots of small files** but you might find yourself in that situation where you do have lots and lots of small files and eventually name nodes will reach their breaking point. There does come a point where a single name node just doesn't cut it.

  So **HDFS Federation** allows you to say okay for these different subdirectories that we're gonna call a **namespace volume** within our HDFS file structure we can actually have **separate name nodes that are responsible for each volume.**

  -> 원래 HD가 최적화되어있던 큰 파일이 아니라, 작고 많은 파일들을 다루는 환경에서 네임노드는 한계에 이를 수 있음. (네임노드는 파일 정보 메타데이터를 메모리에서 관리합니다. 파일이 많아지면 메모리 사용량이 늘어나게 되고, 메모리 관리가 문제가 생김)

  -> HDFS Federation은 namespace volume이라는 것을 만들어서 각각의 볼륨을 책임지는 네임노드를 나눈다. 

  

  And that way a given volume will know which name to talk to for reading and writing data files

   so  we can split. Spread out the load of name nodes if we need to.

   So the relevance here to resilience is that if one of those name notes went down well at least you only. lose a portion of your data. Not all of it.

  

  

  

### HDFS High Availability

* 이중화된 두대의 서버인 액티브(active) 네임노드와 스탠바이(standby) 네임노드를 이용

* 액티브 네임노드와 스탠바이 네임노드는 데이터 노드로부터 블록 리포트와 하트비트를 모두 받아서 동일한 메타데이터를 유지하고, 공유 스토리지를 이용하여 에디트파일을 공유합니다.

  (Running a hot standby name node by using a shared edit log so that your name node is actually writing to some shared storage. That's stored in some reliable file system, not HDFS )

  

* 액티브 네임노드는 네임노드의 역활을 수행하고, 스탠바이 네임노드는 액티브 네임노드와 동일한 메타데이터 정보를 유지하다가, 액티브 네임노드에 문제가 발생하면 스탠바이 네임노드가 액티브 네임노드로 동작하게 됩니다. 

  

* 액티브 네임노드에 문제가 발생하는 것을 자동으로 확인하는 것이 어렵기 때문에 보통 주키퍼를 이용하여 장애 발생시 자동으로 변경될 수 있도록 합니다. (Zookeeper tracks active namenode)

  

* Uses **extreme measures to ensure only one namenode is used at a time**.

* Finally if you can not stand the possibility of some downtime on your cluster at all there is something called HDFS high availability these days and that is actually running a hot standby name node the way

  it does that is by using a shared edit log so that your name node is actually writing to some shared

  storage that's stored in some reliable file system that's not HDFS

  And that way if your name node goes down your hot backup name node can just take over right away.

  And it uses zookeeper which we mentioned briefly in our second lecture to actually keep track of which

  name node is active at a given time so your clients need to talk to zookeeper in this configuration

  to figure out which name should I be talking to for HDFS requests and zookeeper will say OK it's this

  one and it will always make sure that every client is using the same name node at a given time.

  Now there are complications here.

  You know this is a more complicated set up and it has more complicated failure modes as usually happens

  in this case so there are ways of failing where you might actually have two name nodes running at the

  same time.

  And again that can cause very bad things to happen because one node might get a file write request and

  know about where that data is stored.

  And the other one might not.

  So if your read goes to a different name node bad things will happen.

  So to protect against that HDFS high availability actually goes to some extreme measures to make sure

  that only one name is used at a time and you can actually configure it to be so extreme as to actually

  physically cut off the power to a name node that it thinks is down.

  So when zookeeper's says OK I'm switching to this name node it can actually cut the power to the other

  name node to make absolutely sure that no client is still talking to that name node.

  So it's pretty hardcore stuff but obviously that takes a lot of configuration.

  All of this stuff is really relevant more to Hadoop administrators than to you as an application developer

  or an analyst.

  But I just want you to know that the single name node isn't necessarily a big problem there are ways

  of dealing with it such that it's not a single point of failure.





#### Using HDFS

* UI (Ambari)

* Command-Line-Interface

* HTTP/HDFS Proxies

* Java Interface

* NFS GateWay

  * NFS is Network File System

  * mount HDFS to a Linux box and it will just look like you know another mount point on your hard driver system on your file system.

  * so you can actually use programs potentially that don't even

    know about HDFS at all because it will just look like another file on the file system to it using the

    manifest gateway so that's pretty cool stuff too.













