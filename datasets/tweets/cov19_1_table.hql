CREATE DATABASE IF NOT EXISTS testdb1;
USE testdb1;

CREATE EXTERNAL TABLE IF NOT EXISTS cov19_1 (
    id BIGINT,
    hash STRING,
    created_at STRING,
    retweet_count INT,
    favorite_count INT,
    reply_count INT,
    quote_count INT,
    hashtags STRING,
    mentioned_users STRING,
    referenced_tweets STRING,
    external_url STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION 'hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1';
