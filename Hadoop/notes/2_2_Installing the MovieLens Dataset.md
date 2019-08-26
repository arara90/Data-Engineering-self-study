#  Installing the MovieLens Dataset

1. file viewer -> user -> maria-dev > new folder ('ml-100k')
2. u.data, u.item 추가



## Putty

ssh : maria_dev@127.0.0.1:2222

save, load



password : maria_dev 로 접속

hadoop 명령어

* 2_2_001.png

* 2_2_002.png



[upload file local to hdfs]

wget http://media.sundog-soft.com/hadoop/ml-100k/u.data



* 디렉토리 생성

   hadoop fs -mkdir ml-100k

* 목록보기

  hadoop fs -ls

* local에서 hdfs로 올리기

   hadoop fs -copyFromLocal u.data ml-100k/u.data

* 디렉토리 삭제

  hadoop fs -rmdir mk-100ml

* 파일 삭제

  hadoop fs -rm ml-100k/u.data

  

  







