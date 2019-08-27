## Installing python, nano, MRJob

1. hortonwetwork

2. putty

3. su root

4. yum install python-pip

5. Error 발생

   > If above article doesn't help to resolve this issue please open a ticket with Red Hat Support.
   >
   > Error: Cannot retrieve repository metadata (repomd.xml) for repository: sandbox. Please verify its path and try again

[root@sandbox maria_dev]# cd /etc/yum.repos.d
[root@sandbox yum.repos.d]# cp sandbox.repo /tmp
[root@sandbox yum.repos.d]# rm sandbox.repo
rm: remove regular file `sandbox.repo'? y
[root@sandbox yum.repos.d]# cd ~
[root@sandbox ~]# yum install python-pip

 pip install mrjob==0.5.11

안되면 google-api

yum install nano



Resources

http://media.sundog-soft.com/hadoop/RatingsBreakdown.py

http://media.sundog-soft.com/hadoop/u.data





nano RatingsBreakdown.py

python RatingsBreakdown.py u.data

python RatingsBreakdown.py -r hadoop  --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar u.data

[Exercise]

```

from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingsBreakdown(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings),
            MRStep(reducer=self.reducer_sorted_output)
        ]

    def mapper_get_ratings(self, _, line):
        (userID, movieID, rating, timestamp) = line.split('\t')
        yield movieID, 1

    def reducer_count_ratings(self, key, values):
        yield str(sum(values)).zfill(5), key

    def reducer_sorted_output(self, count, movies):
        for movie in movies:
            yield movie, count


if __name__ == '__main__':
    RatingsBreakdown.run()


```

