#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error

class Db:
    """
    sqlite db connection
    """
    def __init__(self, db_file):
        self.db_file = db_file


    def execute(self, sql_command=None, insert_value=None):
        #Open a database connection to a SQLite database.
        #If db_file doesn't exits - db_file will create.
        try:
            conn = sqlite3.connect(self.db_file)
            #return conn
            self.conn = conn
        except Error as e:
            print(e)
            return False

        #Run sql command
        cursor = self.conn.cursor()
        if sql_command and insert_value:
            cursor.execute(sql_command, insert_value)
            self.conn.commit() #save the changes
            return cursor.fetchall()
        elif sql_command:
            cursor.execute(sql_command)
            self.conn.commit() #save the changes
            return cursor.fetchall()
        else:
            #get info about table and rows
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for tbl in tables:
                print "\n######## Table: "+tbl[0]+"  ########"
                cursor.execute("SELECT * FROM "+tbl[0]+";")
                rows = cursor.fetchall()
                for row in rows:
                    print row
            #print(cursor.fetchall())



        #Connection close
        self.conn.close()
