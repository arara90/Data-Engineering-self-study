# Installing Apache Spark and Python

### [ Windows10 기준, Spark 설치하기  + Pycharm ]  

https://sundog-education.com/spark-python/  따라함.



### 1. install JDK

* [http://www.oracle.com/technetwork/java/javase/downloads/index.htm](http://www.oracle.com/technetwork/java/javase/downloads/index.html)[l](http://www.oracle.com/technetwork/java/javase/downloads/index.html)

  > [주의]
  >
  > * 반드시 default location을 변경하여 스페이스('\s')가 없는 경로로 JDK를 설치해줘야한다. (**C:\jdk**)
  >
  > * JAVA 8로 설치할 것. (JAVA 9 이상의 버전에서는 호환이 안된다.)
>
  > * jre도 **C:\jre** 로 변경해주자.
  >
  >   ![jre](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/jrefolder.jpg?raw=true)



### 3. Download a pre-built version of Apache Spark 2.3

* [http://www.rarlab.com/download.ht](http://www.rarlab.com/download.htm)[m](http://www.rarlab.com/download.htm)
* 2.4 버전은 Windows에서 버그가 발생하니 2.3으로 다운로드할 것.



### 4. C:\spark 에 압축 풀어준 것 저장



### 5. C:\tmp\hive\bin 에 winutils.exe 다운로드

* [https://sundo](https://sundog-spark.s3.amazonaws.com/winutils.exe)[g](https://sundog-spark.s3.amazonaws.com/winutils.exe)[–](https://sundog-spark.s3.amazonaws.com/winutils.exe)[s3.amazonaws.com/winutils.ex](https://sundog-spark.s3.amazonaws.com/winutils.exe)[e](https://sundog-spark.s3.amazonaws.com/winutils.exe)

  ![winutils](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/1_4_winutils.jpg?raw=true)



* 다음 cmd창에서 실행 (권한 변경)

```c
	C:\Users\arara>cd c:\tmp\hive\bin
c:\tmp\hive\bin>winutils.exe chmod 777 c:\tmp\hive
```

![chmod](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/chmod.jpg?raw=true)



### 6. C:\spark\conf 에서 log4j.properties 수정

* log4j.properties.templete을 복사해서 templete를 지워주기

![log4j.properties](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/log4j.png?raw=true)

* log4j.rootCategory=INFO 를 log4j.rootCategory=ERROR 로 바꿔주기
  * Error 메세지만 보이도록 로깅 레벨을 낮춤 ![](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/InfotoError.jpg?raw=true)



### 7. 환경변수 추가

 * **SPARK_HOME**

   ![SPARK_HOME)](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/SPARK_HOME.jpg?raw=true)

 * **JAVA_HOME**

   ![JAVA_HOME)](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/JAVA_HOME.jpg?raw=true)

 * **HADOOP_HOME**

   ![HADOOP_HOME)](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/HADOOP_HOME.jpg?raw=true)

   **!!!! 수정 ===>>>> 변수값 : c:\tmp\hive **

    	\bin 추가시 나중에 c:\tmp\hive\bin\bin 으로 찾아가서 에러남.



* PATH

  ![path](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/PATH.jpg?raw=true)



### 8. 확인

* JAVA -  cmd창에서 다음 확인

```
javac -version
java -version
```

![java_finished](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/confirm_java.jpg?raw=true)



> **[문제발생]**
>
> 분명 환경변수를 맞게 설정했고 java는 정상이었으나, javac에서 계속 jvm을 찾지 못했다. 
>
> **원인** : Java Runtime Environment 레지스트리의 javahome 주소가 변경되지 않았다. 
>
> ​			해당 주소의 자바는 이미 삭제한 상태였음.
>
> **해결** : 레지스트리 편집기에서 currentVersion을 확인하고 해당하는 JRE에 가서 직접 수정해주었다.
>
> ![java_reg1](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/java_reg1.png?raw=true)
>
> ![java_reg1](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/java_reg2.png?raw=true)



* SPARK - cmd창에서 다음 확인

```
pyspark  (혹은 spark-shell)
```

![pyspark](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/pyspark.jpg?raw=true)



### 9. Pycharm

file > Settings > project > project Structure > Add Content Root (아래 사진에서 오른쪽 상단)

아래 사진과 같이 Spark를 설치한 경로 내에서 python폴더와, lib 안에 있는 py4j-ver-src.zip파일을 선택하여 추가해준다.

![pycharm](https://github.com/arara90/images/blob/master/TamingBigdataWithSparkAndPython/install/pycharm.jpg?raw=true)



끝!! 

작성된 코드를 run하기만 하면 잘 돌아감!!