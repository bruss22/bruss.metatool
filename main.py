#!/usr/bin/python3
import mysql.connector
import sqlite3
from os.path import exists
from prettytable import PrettyTable
import csv
class tkit:
    def dbConnect(dbname):
        try:
            conn = sqlite3.connect(f'{dbname}')
            #conn = sqlite3.connect(':memory:')
        except Error as e:
            print(e)
        return conn
    def dbExecute(conn,string):
        conn.execute(string)
        conn.commit()
        text = 'OK'
        return text
    def tableState(cur,table):
        try:
            dbstate = cur.execute(f'select * from {table}')
            results = cur.fetchall()
            return results
        except sqlite3.OperationalError as ex:
            dbstate = False
            return dbstate        
    def fileExists(filename):
        filestate = exists(f'{filename}')
        return exists
    def pTable(name,title,header,data):
        name = PrettyTable()
        name.title = title
        name.field_names = header
        for x in data:
            name.add_row(x)
        name.align = "l"
        return name
    def create_table_from_csv(csv_filepath, db_filepath, table_name):
        #borrowed from the internet
        conn = None
        try:
            conn = sqlite3.connect(db_filepath)
            cursor = conn.cursor()
            conn.execute(f'DROP TABLE IF EXISTS {table_name};')
            with open(csv_filepath, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Read the first row as headers
            sanitized_headers = [header.replace(' ', '_').replace('.', '').replace('-', '_') for header in headers]
            columns_definition = ', '.join([f'"{col}" TEXT' for col in sanitized_headers])
            create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})'
            cursor.execute(create_table_sql)
            conn.commit()
            print(f"✅Table '{table_name}' created successfully in '{db_filepath}'.")
            return sanitized_headers
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except FileNotFoundError:
            print(f"Error: CSV file not found at '{csv_filepath}'")
        finally:
            if conn:
                conn.close()
    def sqlite_to_mysql(sqlite_file, mysql_config, mysql_db):
        # borrowed from the internet
        sqlite_conn = sqlite3.connect(sqlite_file)
        sqlite_conn.row_factory = sqlite3.Row  # allows column name access
        sqlite_cursor = sqlite_conn.cursor()
        mysql_conn = mysql.connector.connect(**mysql_config)
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{mysql_db}`")
        mysql_conn.database = mysql_db
        sqlite_cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """)
        tables = [t[0] for t in sqlite_cursor.fetchall()]
        print(f"Found tables: {tables}")
        for table_name in tables:
            print(f"\n=== Migrating table: {table_name} ===")
            sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
            columns = sqlite_cursor.fetchall()
            col_defs = []
            col_names = []
            for col in columns:
                col_name = col[1]
                col_type = col[2].upper() or "TEXT"
                col_names.append(col_name)
                if "INT" in col_type:
                    mysql_type = "INT"
                elif "CHAR" in col_type or "TEXT" in col_type:
                    mysql_type = "VARCHAR(255)"
                elif "REAL" in col_type or "FLOA" in col_type or "DOUB" in col_type:
                    mysql_type = "DOUBLE"
                elif "BLOB" in col_type:
                    mysql_type = "BLOB"
                else:
                    mysql_type = "VARCHAR(255)"
                col_defs.append(f"`{col_name}` {mysql_type}")
            mysql_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
            create_sql = f"CREATE TABLE `{table_name}` ({', '.join(col_defs)});"
            mysql_cursor.execute(create_sql)
            sqlite_cursor.execute(f"SELECT * FROM `{table_name}`;")
            rows = sqlite_cursor.fetchall()
            print(f"  → Found {len(rows)} rows in SQLite table '{table_name}'")
            if rows:
                placeholders = ", ".join(["%s"] * len(col_names))
                insert_sql = f"INSERT INTO `{table_name}` ({', '.join(col_names)}) VALUES ({placeholders})"
                data = [tuple(row[col] for col in col_names) for row in rows]
                mysql_cursor.executemany(insert_sql, data)
                mysql_conn.commit()
                print(f"  ✓ Inserted {len(data)} rows into MySQL table '{table_name}'")
        print("\n✅ Conversion complete!")
        sqlite_conn.close()
        mysql_conn.close()
