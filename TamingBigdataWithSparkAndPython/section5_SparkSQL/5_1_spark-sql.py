from pyspark.sql import SparkSession #Spark 2.0
from pyspark.sql import Row

import collections

# Create a SparkSession (Note, the config section is only for Windows!)
spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("SparkSQL").getOrCreate()

# convert RDDs into Dataframe.
def mapper(line):
    fields = line.split(',')
    # Imparting structure
    return Row(ID=int(fields[0]), name=str(fields[1].encode("utf-8")), age=int(fields[2])
               , numFriends=int(fields[3]))


lines = spark.sparkContext.textFile("file:///TamingBigdataWithSparkAndPython/data/fakefriends.csv") # is not structured.
people = lines.map(mapper)

# Infer the schema, and register the DataFrame as a table.
# .cache() : because we're under more than one thing to it.
#            because we're gonna reuse that schemaPeople Df, we're gonna cache thar
schemaPeople = spark.createDataFrame(people).cache()

# Create sort of a temporary SQL table in momory called people that we can issue.
schemaPeople.createOrReplaceTempView("people")

# SQL can be run over DataFrames that have been registered as a table.
teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")

# The results of SQL queries are RDDs and support all the normal RDD operations.
for teen in teenagers.collect():
  print(teen)

# We can also use functions instead of SQL queries:
schemaPeople.groupBy("age").count().orderBy("age").show()

spark.stop()
