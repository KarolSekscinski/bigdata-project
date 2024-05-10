#!/bin/bash
hive -e "DROP TABLE IF EXISTS testdb1.who;
	DROP DATABASE IF EXISTS testdb1;"