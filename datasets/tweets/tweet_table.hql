create database if not exists testdb1;
use testdb1;
create external table if not exists tweet (
    tweet_id int,
    created_at date,
    source string,
    original_text string,
    lang string,
    favourite_count int,
    retweet_count int,
    original_author string,
    hashtags string,
    user_mentions string,
    place string,
    clean_tweet string,
    compound float,
    neg float,
    neu float,
    pos float,
    sentiment string
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/testdb1.db/tweet';