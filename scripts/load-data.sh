# Connect to the hive-server container and execute commands
docker exec -it hive-server /bin/bash -c @"
    cd ../who
    hive -f who_table.hql
    hadoop fs -put who_data.csv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/who
"@
