# -*- coding: utf-8 -*-

import psycopg2, os

# Classes

class datasetting:
      
    def __init__(self, database, host, port, user, password):

        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.connectPostgreSql = psycopg2.connect(
                database = self.database,
                host = self.host,
                user = self.user,
                password = self.password,
                port = self.port
            )
        
        self.cursor = self.connectPostgreSql.cursor()

        self.connectPostgreSql.autocommit = True

    def createtable(self, table_list):
        
        for table in table_list:

            try:
                self.cursor.execute(f'CREATE TABLE {table} ({table_list[table]})')
            except:
                continue

    def getdata(self, table_name, special_stroke):
         
        if special_stroke.lower() == 'default':
             
            special_stroke = '*'
        
        self.cursor.execute(f"SELECT {special_stroke} FROM {table_name}")

        count = 0

        while True:

            count += 1
            
            try:

                data = self.cursor.fetchall()
                break

            except:

                pass

        return data

    def deldata(self, table_name, stroke_name, data_name):
         
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {stroke_name} = '{data_name}'")
    
    def insertdata(self, table_name, stroke_list, data_list):
         
        self.cursor.execute(f"INSERT INTO {table_name} ({stroke_list}) VALUES ({data_list})")

    def updatedata(self, table_name, stroke_name, data_name):
         
        self.cursor.execute(f"UPDATE {table_name} SET {stroke_name} = '{data_name}'")

    def closepsql(self):

        self.connectPostgreSql.commit()
        self.connectPostgreSql.close()
        self.cursor.close()

# Functions

def createDB():

    try: 
        connectPostgreSql = psycopg2.connect(
                host="localhost",
                port="5432",
                user= "postgres",
                password= "postgres")
    except:
        os.system("PostgreSQL.exe")
        connectPostgreSql = psycopg2.connect(
        host="localhost",
        port="5432",
        user= "postgres",
        password = "postgres")

    try:
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
            connectPostgreSql.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connectPostgreSql.cursor()
            sql_create_database = 'create database settings'
            cursor.execute(sql_create_database)
            cursor.close()
    except: 
            pass
    
    connectPostgreSql.close()

    connectPostgreSql = psycopg2.connect(
            database="settings",
            host="localhost",
            port="5432",
            user= "postgres",
            password= "postgres"
    )

    connectPostgreSql.close()

def blockIpList():

    conn = psycopg2.connect(
            database="settings",
            host="localhost",
            port="5432",
            user= "postgres",
            password= "postgres")

    cursor = conn.cursor()
    conn.autocommit = True

    cursor.execute('SELECT blockip FROM blockipsinfo')
    data = cursor.fetchall()

    block_ip_list = []

    for ip in data:

        block_ip_list.append(ip[0])

    conn.commit()
    cursor.close()
    conn.close()

    return block_ip_list

def workIpList():

    conn = psycopg2.connect(
        database="settings",
        host="localhost",
        port="5432",
        user= "postgres",
        password= "postgres")

    cursor = conn.cursor()
    conn.autocommit = True

    cursor.execute('SELECT workip FROM workipsinfo')
    data = cursor.fetchall()

    work_ip_list = []

    for ip in data:

        work_ip_list.append(ip[0])

    conn.commit()
    cursor.close()
    conn.close()

    return work_ip_list

table_list = {  
                'mainsetting':'id SERIAL PRIMARY KEY, accesskey TEXT, secretkey TEXT, tgid TEXT, bottoken TEXT, region TEXT',
                'agrosettings':'id SERIAL PRIMARY KEY, name TEXT, accesskey TEXT, secretkey TEXT', 
                'workipsinfo':'id SERIAL PRIMARY KEY, workip TEXT, workset TEXT', 
                'blockipsinfo':'id SERIAL PRIMARY KEY, blockip TEXT, blocksubset TEXT', 
                'accountdata':'id SERIAL PRIMARY KEY, login TEXT, password TEXT, uid TEXT',
                'regions':'id SERIAL PRIMARY KEY, regionuser TEXT'
             }

createDB()
postgresql = datasetting('settings', 'localhost', '5432', 'postgres', 'postgres')
postgresql.createtable(table_list)
