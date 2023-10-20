import sqlite3
from cryptography.fernet import Fernet

with open("key.key", "rb") as file:
    key = file.read()
fernett = Fernet(key)
class Database:

    def connect_to_db(self):
        conn = sqlite3.connect("password_database.db")
        return conn

    def create_table(self, table_name="password_records"):
        conn = self.connect_to_db()
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                website TEXT NOT NULL,
                username VARCHAR(200),
                password BLOB
            );
        '''
        with conn as con:
            cursor = con.cursor()
            cursor.execute(query)

    def create_record(self, data, table_name="password_records"):
        website = data["website"]
        username = data["username"]
        password = data["password"]
        conn = self.connect_to_db()
        query = f'''
            INSERT INTO {table_name} ("website", "username", "password") VALUES (?, ?, ?)
        '''
        with conn as con:
            cursor = con.cursor()
            cursor.execute(query, (website, username, fernett.encrypt(password)))
            conn.commit()

    def update_record(self, data, table_name="password_records"):
        ID = data["ID"]
        website = data["website"]
        username = data["username"]
        password = data["password"]
        conn = self.connect_to_db()
        query = f'''
            UPDATE {table_name} SET website = ?, username = ?, password = ? WHERE ID = ?
        '''
        with conn as con:
            cursor = con.cursor()
            cursor.execute(query, (website, username, fernett.encrypt(password), ID))
            conn.commit()

    def delete_record(self, ID, table_name="password_records"):
        conn = self.connect_to_db()
        query = f'''
            DELETE FROM {table_name} WHERE ID = ?
        '''
        with conn as con:
            cursor = con.cursor()
            cursor.execute(query, (ID,))
            conn.commit()

    def search_record(self, website, table_name="password_records"):
        conn = self.connect_to_db()
        query = f'''
            SELECT * FROM {table_name} WHERE website LIKE "%{website}%"
        '''
        with conn as con:
            cursor = con.cursor()
            search_records = cursor.execute(query).fetchall()
            return search_records

    def show_records(self, table_name="password_records"):
        conn = self.connect_to_db()
        query = f'''
            SELECT * FROM {table_name}
        '''
        with conn as con:
            cursor = con.cursor()
            records = cursor.execute(query)
            return records
