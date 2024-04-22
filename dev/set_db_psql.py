#!/usr/bin/env python3
""" Script to setup the Postgresql database

    Notes:
        For this script to work, the env_var.sh must be set,
        also make sure to run it from run_setup_db.sh.
        *This script will create the user and the database*
    Important:
        Ensure that pg_hba.conf is configured
         to allow the user to connect(trust)
"""


from os import getenv
import psycopg2


def create_user(db_user, db_password):
    """ Create the user as superuser """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres"
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            f"CREATE USER {db_user} WITH LOGIN PASSWORD '{db_password}';"
        )
        cur.execute(f"ALTER USER {db_user} CREATEDB;")

        print(f"User {db_user} created successfully")
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error creating user: {e}")


def create_db(db_name, db_user, db_password, db_host, db_port):
    """ Create the database """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            host=db_host,
            password=db_password,
            port=db_port,
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"CREATE DATABASE {db_name} OWNER {db_user};")

        print(f"Database {db_name} created successfully")
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")


if __name__ == "__main__":
    db_name = getenv("POSTGRES_DB")
    db_user = getenv("POSTGRES_USER")
    db_password = getenv("POSTGRES_PASSWORD")
    db_host = getenv("POSTGRES_HOST")
    db_port = getenv("POSTGRES_PORT")
    create_user(db_user, db_password)
    create_db(db_name, db_user, db_password, db_host, db_port)
