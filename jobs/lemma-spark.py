from pyspark.sql import SparkSession
from transformers import pipeline
from pyspark.sql.functions import concat_ws

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

# Create a SparkSession
spark = SparkSession.builder \
    .appName("Fine-tuning Hugging Face model") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# Set the database to 'testdb1'
spark.sql("USE testdb1")

# Query the 'who' table and load data into a DataFrame
df = spark.sql("SELECT * FROM tweets limit 5;")

# Concatenate rows into a single string
concatenated_df = df.select(concat_ws(",", *df.columns).alias("concatenated_row"))

# Show the concatenated DataFrame
concatenated_df.show(truncate=False)
for row in concatenated_df.collect():
    sequence_to_classify = row
    candidate_labels = ['real', 'fake']
    classifier(sequence_to_classify, candidate_labels, multi_label=False)
    print(sequence_to_classify['scores'], row)
    print()
    print()
    print()
    print()
    print()


# def tokenize_function(examples):
#     return tokenizer(examples["Country"], padding="max_length", truncation=True)


