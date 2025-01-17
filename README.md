# Big Data COVID-19 Analysis Platform

A comprehensive big data platform for analyzing COVID-19 related tweets and WHO data using Apache Spark, Hadoop, and Hive.

## Overview

This project sets up a distributed data processing environment to analyze COVID-19 related data from multiple sources:
- Twitter data about COVID-19
- WHO official COVID-19 statistics
- Sentiment analysis and classification of tweets

## Architecture

The platform consists of the following components:
- Apache Spark cluster (1 master + 2 workers)
- Apache Hadoop (HDFS)
- Apache Hive with PostgreSQL metastore
- Apache Airflow for workflow orchestration

## Prerequisites

- Docker and Docker Compose
- Python 3.x
- At least 8GB RAM available

## Project Structure

```
.
├── dags/                   # Airflow DAG definitions
│   ├── example.py         # Example DAG with simple tasks
│   └── preprocess_kaggle_data.py  # Data preprocessing pipeline
├── datasets/              
│   ├── tweets/            # Twitter dataset location
│   └── data-who/          # WHO dataset and HQL scripts
├── jobs/                  # Spark jobs
│   ├── lemma-spark.py     # Text analysis using transformers
│   └── load-data-spark.py # Data loading operations
├── notebooks/             # Analysis notebooks
├── scripts/               # Utility scripts
├── docker-compose.yml     # Container orchestration
├── Dockerfile.spark       # Spark image configuration
└── hadoop-hive.env        # Environment configuration
```

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/KarolSekscinski/bigdata-project.git
cd <repository-name>
```

2. Create necessary directories:
```bash
mkdir -p hdfs/namenode hdfs/datanode
mkdir -p metastore-postgresql/postgresql/data
```

3. Start the containers:
```bash
docker-compose up -d
```

## Data Loading

Load data into HDFS and Hive:
```bash
./scripts/load-data-docker.sh
```

## Available Scripts

- `load-data.sh`: Loads tweets and WHO data into HDFS
- `delete_who.sh`: Cleans up WHO data tables
- `load-data-cov19.sh`: Loads COVID-19 specific datasets

## Spark Jobs

- `load-data-spark.py`: Loads data from Hive into Spark
- `lemma-spark.py`: Performs text analysis on tweets

## Analysis Notebooks

- `check_truth.py`: Validates death statistics between sources
- `classification.py`: Classifies tweets using transformers

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- WHO for providing COVID-19 data
- Twitter for the tweet datasets
- The Apache Software Foundation for Spark, Hadoop, and Hive/
