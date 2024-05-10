--example table for who data file WHO-COVID-19-global-data
--https://covid19.who.int/WHO-COVID-19-global-data.csv
create database if not exists testdb1;
use testdb1;
create external table if not exists who (
    date_reported date,
    country_code string,
    country_name string,
    who_region string,
    new_cases int,
    cumulative_cases int,
    new_deaths int,
    cumulative_deaths int
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/testdb1.db/who';