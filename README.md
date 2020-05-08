# Cloud Data Warehouse with Amazon Redshift 

### Summary

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

We need to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. Test the database and ETL pipeline by running queries.

### Project Description

Build an ETL pipeline for a Data Warehouse database hosted on AWS Redshift. We will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

### Pre-Requisites
* AWS Redshift Cluster, IAM Role (Read Amazon S3), Security Group (Allow Inbound)
* Ensure psycopg2 is installed in a python3 environment
* Jupyter Notebook (Testing)

### How to Run & Test

* Use Run-ETL.ipynb (Jupyter Notebook) to connect to Redshift and Run ETL Pipeline. 
* Run first two cells of Run-ETL.ipynb to create & load staging & fact-dimension tables onto the database.
* Run remaining cells to run various queries over the sparkify music database

### Files
| Filename |  |
| ------ | ------ |
| sql_queries.py | Redshift queries to create & drop tables, Copy & Insert data into the tables, etc. | 
| create_tables.py | Ensures clean database, connection and create tables. |
| etl.py: | Extract (Copy song & log datafiles from S3 onto staging tables on Redshift), Transform & Load (Create Fact-Dimension Tables and Insert data). |
| RunETL.ipynb | Setup Database and Run ETL Pipeline |
| dwf.dfg | Config file with AWS S3 & Redshift parameters. |


### Acknowledgement
Author: Hari Raja
Framework: Udacity
Date: May 7 2020
