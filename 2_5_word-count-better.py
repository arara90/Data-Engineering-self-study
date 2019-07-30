# can use natural language processing toolkit NLTK
# but we'll keep it simple, and use a regular expression


import re # regular expression : https://wikidocs.net/1669 공부하기
from pyspark import SparkConf, SparkContext

def normalizeWords(text):
    # And in our case we're going to call re.compile and this is the magical string that means I want to
    # you to break up this text based on words and the W+ capital W+ indicates.
    # Break it up based on words and the regular expression engine knows on its own how to do that
    # and strip out punctuation and other things that aren't really part of words automatically
    # -> 즉, 단어 단위로 쪼개고, .이나 다른 특수문자같이 단어의 일부분이 아닌것들을 자동으로 없애준다.
    # We'll tell them that this may have Unicode information in it and then we will split it up you know
    # based on what the regular expression identifies as individual words and transform those all to lowercase.

    # \W+ 문자 또는 숫자가 아닌것?
    return re.compile(r'\W+', re.UNICODE).split(text.lower())

conf = SparkConf().setMaster("local").setAppName("WordCount")
sc = SparkContext(conf = conf)

input = sc.textFile("file:///TamingBigdataWithSparkAndPython/data/book.txt")
words = input.flatMap(normalizeWords)

# print(words.collect())


wordCounts = words.countByValue()
for word, count in wordCounts.items():
    cleanWord = word.encode('ascii', 'ignore')
    if (cleanWord):
        print(cleanWord.decode() + " " + str(count))
