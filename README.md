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
| dwf.cfg | Config file with AWS S3 & Redshift parameters. |

### Table Design
##### Staging Tables  
- staging_events_table
- staging_songs_table

##### Dimension Tables
- songs
- artists
- users
- times

##### Facts Table
- songplays

##### DISTKEY, SORTKEY
- artist_id (or artist name) used for distribution
- song_id, artist_id, user_id, timestamp, songplay_id used for sorting

```sh
# store raw data from log_data JSON files on S3 onto staging_events_table 
CREATE TABLE IF NOT EXISTS staging_events_table (
    "artist" varchar,
    "auth" varchar, 
    "firstname" varchar, 
    "gender" varchar, 
    "iteminsession" int,
    "lastname" varchar, 
    "length" real, 
    "level" varchar, 
    "location" varchar, 
    "method" varchar, 
    "page" varchar, 
    "registration" bigint, 
    "sessionid" bigint, 
    "song" varchar, 
    "status" int, 
    "ts" bigint, 
    "useragent" varchar(512), 
    "userid" bigint
) DISTKEY(artist)

# store raw data from song_data JSON files on S3 onto staging_songs_table 
CREATE TABLE IF NOT EXISTS "staging_songs_table" (
    "song_id" varchar,
    "title" varchar(512), 
    "num_songs" int, 
    "year" int, 
    "duration" real,
    "artist_id" varchar, 
    "artist_name" varchar(512), 
    "artist_location" varchar(512), 
    "artist_latitude" real, 
    "artist_longitude" real
) DISTKEY(artist_id) SORTKEY(song_id)

# records in log data associated with song plays i.e. records with page 'NextSong'
# ensure that a user is using a single session at any particular time
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id int IDENTITY(1,1) PRIMARY KEY, 
    start_time bigint NOT NULL, 
    user_id bigint NOT NULL, 
    song_id varchar, 
    artist_id varchar, 
    session_id bigint NOT NULL, 
    location varchar, 
    user_agent varchar(512),
    UNIQUE (start_time, user_id, session_id)
) DISTKEY(artist_id) SORTKEY(songplay_id)

# users in the app
CREATE TABLE IF NOT EXISTS users (
    user_id bigint PRIMARY KEY, 
    first_name varchar, 
    last_name varchar, 
    gender varchar, 
    level varchar
) SORTKEY(user_id)

# songs in music database
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY, 
    title varchar(512), 
    artist_id varchar, 
    year int, 
    duration real
) DISTKEY(artist_id) SORTKEY(song_id)

# artists in music database
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY, 
    name varchar(512), 
    location varchar(512), 
    latitude real, 
    longitude real
) SORTKEY(artist_id)

# timestamps of records in songplays broken down into specific units
CREATE TABLE IF NOT EXISTS times (
    start_time bigint PRIMARY KEY, 
    dt DATE NOT NULL, 
    hour smallint NOT NULL, 
    day smallint NOT NULL, 
    week smallint NOT NULL, 
    month smallint NOT NULL, 
    year smallint NOT NULL, 
    weekday boolean NOT NULL
) SORTKEY(start_time)
```

### Acknowledgement
Author: Hari Raja
Framework: Udacity
Date: May 7 2020
