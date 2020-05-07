import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

REGION           = config.get('AWS','REGION')
IAM_ROLE_ARN     = config.get('IAM_ROLE','ARN')

LOG_DATA         = config.get('S3','LOG_DATA')
LOG_JSONPATH     = config.get('S3','LOG_JSONPATH')
SONG_DATA        = config.get('S3','SONG_DATA')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS times"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events_table \
(artist varchar, auth varchar, firstName varchar, gender varchar, itemInSession int, lastName varchar, \
length real, level varchar, location varchar, method varchar, page varchar, registration bigint, \
sessionId bigint, song varchar, status int, ts bigint, userAgent varchar(512), userId bigint)
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs_table \
(song_id varchar, title varchar(512), num_songs int, year int, duration real, artist_id varchar, \
artist_name varchar(512), artist_location varchar(512), artist_latitude real, artist_longitude real) DISTKEY (year)
""")

# records in log data associated with song plays i.e. records with page 'NextSong'
# ensure that a user is using a single session at any particular time
songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays \
(songplay_id int IDENTITY(1,1) PRIMARY KEY, start_time bigint NOT NULL, user_id bigint NOT NULL, \
song_id varchar, artist_id varchar, session_id bigint NOT NULL, location varchar, user_agent varchar(512), \
UNIQUE (start_time, user_id, session_id))""")

# users in the app
user_table_create = ("""CREATE TABLE IF NOT EXISTS users \
(user_id bigint PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar) \
""")

# songs in music database
song_table_create = ("""CREATE TABLE IF NOT EXISTS songs \
(song_id varchar PRIMARY KEY, title varchar(512), artist_id varchar, year int, duration real) \
""")

# artists in music database
artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists \
(artist_id varchar PRIMARY KEY, name varchar(512), location varchar(512), latitude real, longitude real) \
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS times \
(start_time bigint PRIMARY KEY, dt DATE NOT NULL, hour smallint NOT NULL, day smallint NOT NULL, \
week smallint NOT NULL, month smallint NOT NULL, year smallint NOT NULL, weekday boolean NOT NULL) \
""")

# STAGING TABLES

staging_songs_copy = ("""COPY staging_songs_table FROM {}
    CREDENTIALS 'aws_iam_role={}'
    JSON 'auto'
    REGION '{}'
""").format(SONG_DATA, IAM_ROLE_ARN, REGION)

staging_events_copy = """
    COPY staging_events_table FROM {}
    CREDENTIALS 'aws_iam_role={}'
    JSON {}
    REGION '{}'
""".format(LOG_DATA, IAM_ROLE_ARN, LOG_JSONPATH, REGION)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, song_id, artist_id, session_id, location, user_agent)
SELECT DISTINCT se.ts AS start_time, se.userId AS user_id, sst.song_id AS song_id, sst.artist_id AS artist_id, \
    se.sessionId AS session_id, se.location AS location, se.userAgent AS user_agent
FROM staging_events_table se
JOIN staging_songs_table sst
ON sst.title=se.song AND sst.artist_name=se.artist AND ROUND(sst.duration)=ROUND(se.length) 
WHERE se.page='NextSong'
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT se.userId AS user_id, se.firstName AS first_name, se.lastName AS last_name, \
    se.gender AS gender, se.level AS level
FROM staging_events_table se
WHERE se.page='NextSong'
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT sst.song_id AS song_id, sst.title AS title, sst.artist_id AS artist_id, \
    sst.year AS year, sst.duration AS duration
FROM staging_songs_table sst
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT sst.artist_id AS artist_id, sst.artist_name AS name, sst.artist_location AS location, \
    sst.artist_latitude AS latitude, sst.artist_longitude AS longitude
FROM staging_songs_table sst
""")

time_table_insert = ("""
INSERT INTO times (start_time, dt, hour, day, week, month, year, weekday)
SELECT 
       DISTINCT se.ts                      AS start_time,
       DATEADD(ms, CAST(se.ts as bigint), '1970-01-01') AS dt,
       EXTRACT(hour FROM dt)               AS hour,
       EXTRACT(day FROM dt)                AS day,
       EXTRACT(week FROM dt)               AS week,
       EXTRACT(month FROM dt)              AS month,
       EXTRACT(year FROM dt)               AS year,
       CASE WHEN EXTRACT(dayofweek FROM dt) IN (6, 7) THEN false ELSE true END AS weekday
FROM staging_events_table se
WHERE se.page='NextSong'
""")


# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = []
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

# create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
# drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
# copy_table_queries = [staging_events_copy, staging_songs_copy]
# insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
