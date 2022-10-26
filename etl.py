import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    """
    Load staging tables from S3 bucket
    
    Parameters
    ----------
    cur : cursor of psycopg2 database connection
    conn : connection of psycopg2
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Load final tables from staging tables
    
    Parameters
    ----------
    cur : cursor of psycopg2 database connection
    conn : connection of psycopg2
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
     Read credentials from dwh.cfg config file.
     Load staging tables from S3.
     Loading final tables from staging tables.   
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