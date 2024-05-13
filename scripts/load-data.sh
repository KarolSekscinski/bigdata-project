#!/bin/bash
hive -f /tweets/tweet_table.hql
hive -f /who/who_table.hql
hive -f /tweets/cov19_1_table.hql

# Function to check if a file exists in HDFS
file_exists_in_hdfs() {
    hdfs dfs -test -e "$1"
}

# Function to copy file to HDFS if it doesn't exist
copy_to_hdfs_if_not_exists() {
    if ! file_exists_in_hdfs "$2"; then
        echo "Copying $1 to HDFS..."
        hadoop fs -put "$1" "$2"
    else
        echo "$1 already exists in HDFS."
    fi
}

# Load big tweets from tsv
copy_to_hdfs_if_not_exists "/tweets/TweetsCOV19_1.tsv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1"
copy_to_hdfs_if_not_exists "/tweets/TweetsCOV19_2.tsv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1"
copy_to_hdfs_if_not_exists "/tweets/TweetsCOV19_3.tsv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1"
copy_to_hdfs_if_not_exists "/tweets/TweetsCOV19_4.tsv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1"

# Load tweets from kaggle
copy_to_hdfs_if_not_exists "/tweets/clean_tw-1.csv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/tweet"
copy_to_hdfs_if_not_exists "/tweets/clean_tw-2.csv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/tweet"
copy_to_hdfs_if_not_exists "/tweets/clean_tw-3.csv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/tweet"

# Load who data
copy_to_hdfs_if_not_exists "/who/who_data.csv" "hdfs://namenode:8020/user/hive/warehouse/testdb1.db/who"

#hadoop fs -put /tweets/TweetsCOV19_1.tsv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1
#hadoop fs -put /tweets/TweetsCOV19_2.tsv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1
#hadoop fs -put /tweets/TweetsCOV19_3.tsv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1
#hadoop fs -put /tweets/TweetsCOV19_4.tsv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1
#
#hadoop fs -put /who/who_data.csv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/who
#
#hadoop fs -put /tweets/clean_tw-1.csv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/tweet
#hadoop fs -put /tweets/clean_tw-2.csv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/tweet
#hadoop fs -put /tweets/clean_tw-3.csv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/tweet