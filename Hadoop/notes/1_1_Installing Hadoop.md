##  Installing Hadoop [Step by Step]

참고 : <https://sundog-education.com/hadoop-materials/>

### Data set Download

<https://grouplens.org/datasets/movielens/>

![img6.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img6.png?raw=true)

- download - older Data - ml-100k.zip



### Using VirtualBox

<https://www.virtualbox.org/wiki/Downloads>

![oracleVM.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/oracleVM.png?raw=true)



* HDP(Hortonworks Data Platform)을 돌리기위해 **최소 8GB의 RAM**이 필요함. 

  > * **Hortonworks Data Platform(HDP)**은 엔터프라이즈가 정형 및 비정형 데이터로부터 통찰력을 확보할 수 있도록 지원합니다. 이는 방대한 멀티소스 데이터 세트를 분산 저장하고 처리할 수 있는 오픈 소스 프레임워크입니다. HDP는 IT 인프라를 현대화하고 클라우드 또는 온프레미스에 데이터 보안을 유지하는 한편, 새로운 매출 흐름을 주도하고 고객 경험을 개선하여 비용을 제어할 수 있도록 지원합니다.
  >
  >   HDP는 민첩한 애플리케이션 배포, 머신 러닝 및 딥러닝 워크로드, 실시간 데이터 웨어하우징, 보안, 거버넌스를 선사합니다. 이는 비활성 데이터에 맞는 현대적 데이터 아키텍처의 핵심 구성요소입니다.

* Avast 백신 프로그램 사용중이라면, Virtual Box와 충돌이 있음!

* BIOS setting 에서 Virtualization이 enable인지 확인! 
  * ''노트북 제조사명(Lenovo) BIOS 가상화'' 등으로 검색해보기
    * Lenovo -> 부팅시 빠르게 F2 눌러서 들어가서 설정해줌!
  * 설정 변경 시 재시작 필요함. 
* Hyper-v 가상화 장치가 있다면 문제 발생할 수 있음

* 가상머신 종료시 Power Off 말고, ACPI shutdown 사용할것! or just simply pause the image! 



### Cloudera 

<https://www.cloudera.com/downloads.html>

![img3.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img3.png?raw=true)



#### Hortonworks Sandbox 다운로드하기!

![img4.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img4.png?raw=true)

* Virtualbox 선택

* 더 적은 자원을 사용하고, lecture를 안정적으로 따라가기 위해서 Older version인 2.5.0 선택



* 다운로드한 파일 실행 -> 가져오기(import)를 눌러서 VM안으로 가져옴!

  ![img5.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img5.png?raw=true)

  * pre-installed Hadoop environment .. 이미 설치되어 있음!

    

* import 완료되면 해당 VM 실행 후 host PC(VM 밖의 PC)에서 인터넷 창 실행

*  <http://127.0.0.1:8888/>

  ![img2-1.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-1.png?raw=true)

*  Sign in => ID/ PW : maria_dev / maria_dev



#### Ambari 사용해보기!

**Dashboard**

![img2-2.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-2.png?raw=true)

**Table 업로드**

* (우측 상단)그리드 아이콘 > Hive View(사진) > Upload Table

  ![img2-3.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-3.png?raw=true)

  

  * File type:CSV 

  * 파일 선택 -> u.data (처음에 다운받은 데이터 중에서)

  * 설정(아이콘) -> Filed Delimiter(구분기호) :  9 Tab

    ![img2-4.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-4.png?raw=true) 

  * 테이블 명(rating), 컬럼명 (user_id, movie_id, rating, rating_time) 변경

  ![img2-5.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-5.png?raw=true)

  

* Upload Table

  ![img2-6.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-6.png?raw=true)

  

* u.item도 upload하기

  - 설정(아이콘) -> Filed Delimiter(구분기호) :  124 |
  - 파일 선택 -> u.item(처음에 다운받은 데이터 중에서)
  - 테이블 명(movie_names), 컬럼명 (movie_id,name) 변경



**Query로 확인해보기!** 

![img2-8.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-8.png?raw=true)



* [추가] 자유롭게 Query로 확인해보기!  

```sql
SELECT A.movie_id, B.name, count(A.movie_id) as ratingCount
FROM ratings as A, movie_name as B
WHERE A.movie_id = B.movie_id
GROUP BY A.movie_id, B.name 
ORDER BY ratingCount
DESC;
```

![img2-10.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-10.png?raw=true)





**Visualization 사용해보기**

* Columns의 항목을 positional에 드래그 해 본 결과

![img2-9.png](https://github.com/arara90/images/blob/master/TheUltimateHandsonHadoop-TameYourBingData/img2-9.png?raw=true)

