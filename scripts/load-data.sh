#!/bin/bash
ls .
hive -f /who/who_table.hql
hadoop fs -put /who/who_data.csv hdfs://namenode:8020/user/hive/warehouse/testdb1.db/who