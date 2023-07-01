import mysql.connector
import os

HOST = os.environ['DB_HOST']
PASSWORD = os.environ['DB_PASSWORD']
USER = os.environ['DB_USER']
DATABASE = os.environ['DB']

class Database():
    def __init__(self, table_name) -> None:
        self.table_name = table_name

    def connect(self):
        return mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
    
    def select(self, fields:str, condictionals:str, *values):
        sql = f"SELECT {fields} FROM {self.table_name} WHERE {condictionals}"
        connection = self.connect()

        cursor = connection.cursor()

        print(f"Execute {sql}")
        print(values)
        cursor.execute(sql, values)

        result = cursor.fetchall()

        cursor.close()
        connection.close()
        
        return result
    
    def select_one(self, fields:str, condictionals:str, *values):
        sql = f"SELECT {fields} FROM {self.table_name} WHERE {condictionals}"
        connection = self.connect()

        cursor = connection.cursor()

        print(f"Execute {sql}")
        print(values)
        cursor.execute(sql, values)

        result = cursor.fetchone()

        cursor.close()
        connection.close()
        
        return result
    
    def insert(self, fields:str, *values):
        sql = f"INSERT INTO {self.table_name} ({fields}) VALUES ({','.join(['%s' for _ in range(len(values))])})"
        connection = self.connect()

        cursor = connection.cursor()

        print(f"Execute {sql}")
        print(values)
        cursor.execute(sql, values)
        
        connection.commit()
        column_id = cursor.lastrowid
        print(cursor.rowcount, "record inserted.")
        print(column_id)

        cursor.close()
        connection.close()
        return column_id
    
    def update(self, fields:str, *values):
        sql = f"UPDATE {self.table_name} SET {fields} WHERE request_id = %s"
        connection = self.connect()

        cursor = connection.cursor()
        print(f"Execute {sql}")
        print(values)
        cursor.execute(sql, values)

        connection.commit()
        column_id = cursor.lastrowid

        cursor.close()
        connection.close()
        return column_id