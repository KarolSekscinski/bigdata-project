#!/bin/bash
docker exec -it hive-server /bin/bash -c '
    cd /tweets
    hive -f cov19_1_table.hql
    hadoop fs -put cov19_1.tsv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/cov19_1
'