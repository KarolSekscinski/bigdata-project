import sys
from pyspark.sql import SparkSession



# Create a SparkSession
spark = SparkSession.builder \
    .appName("Accessing Hive Data") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# Set the database to 'testdb1'
spark.sql("USE testdb1")

# Query the 'who' table for the first 100 records and load data into a DataFrame
df = spark.sql("SELECT * FROM who LIMIT 100")

# Perform further operations on the DataFrame as needed
df.show()
# Close the output file
table_name = "res_who"
df.write.mode("overwrite").saveAsTable(table_name)



