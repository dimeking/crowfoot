import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    - Transfer all song json data files on S3 to a staging table on Redshift
    - Transfer all log json data files on S3 to a staging table on Redshift
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    - Transform relevant data from staging songs table to dimension tables (songs, artists)
    - Transform relevant data from staging events table to dimension tables (users, times)
    - Transform relevant data from staging events table to fact table (songplays)
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Reads config file to collect AWS Redshift database params.     
    - Establishes connection with the sparkify database and gets
    cursor to it.      
    - load all the staging tables on Redshift from S3 json files.      
    - Transform all the relevant data from staging tables to Dimension & Tables on Redshift.     
    - Finally, closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()