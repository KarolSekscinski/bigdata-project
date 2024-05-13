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
df = spark.sql("SELECT * FROM tweet limit 150;")
tweets = [row.original_text for row in df.select('original_text').limit(10).collect()]
print(tweets)
# print(tweet)
candidate_labels = ['covid','politics','death','infection']
results = []
for i,tweet in enumerate(tweets[1:]):
    result = classifier(tweet, candidate_labels)
    label_score_pairs = [(label, score) for label, score in zip(result['labels'], result['scores'])]
    label_score_pairs.insert(0,result['sequence'])
    # sorted_results = sorted(label_score_pairs, key=lambda x: x[1], reverse=True)
    results.append(label_score_pairs)
    print(i)
# print(results)
# sorted_results = sorted(results, key=lambda x: x[0][1], reverse=True)

for item in results:
    print(item[0])
    print(item[1:])
    print()

# # Concatenate rows into a single string
# concatenated_df = df.select(concat_ws(",", *df.columns).alias("concatenated_row"))

# # Show the concatenated DataFrame
# concatenated_df.show(truncate=False)
# for row in concatenated_df.collect():
#     sequence_to_classify = row
#     candidate_labels = ['real', 'fake']
#     classifier(sequence_to_classify, candidate_labels, multi_label=False)
#     print(sequence_to_classify['scores'], row)
#     print()
#     print()
#     print()
#     print()
#     print()


# def tokenize_function(examples):
#     return tokenizer(examples["Country"], padding="max_length", truncation=True)


