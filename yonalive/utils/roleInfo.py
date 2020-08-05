import os
import sqlite3

DATABASE = os.getcwd()+'/databases/role.db'
TABLE = "Roles"

class RoleDB:
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild

        self.conn = None

        try:
            self.conn = sqlite3.connect(DATABASE)
        except sqlite3.Error as e:
            print(e)
        self.cursor = self.conn.cursor()


        self._create_table()
        self._get_role()

    def close(self):
        self.conn.close()
        del self

    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE} (id BIGINT, bool INT, role TEXT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def _get_role(self):
        query = f"SELECT * FROM {TABLE} WHERE id = ?"
        self.cursor.execute(query, (self.guild.id,))
        info = self.cursor.fetchall()
        if info:
            self.role = info[0][2]
            return self.role
        else:
            self._create_role()
            self._get_role()

    def _get_bool(self):
        query = f"SELECT * FROM {TABLE} WHERE id = ?"
        self.cursor.execute(query, (self.guild.id,))
        info = self.cursor.fetchall()
        if info:
            self.bool = info[0][1]
            return self.bool
        else:
            self._create_role()
            self._get_role()


    def _create_role(self):
        try:
            query = f"""INSERT INTO {TABLE} VALUES (?, ?, ?)"""
            self.cursor.execute(query, (self.guild.id, 0, ''))
            self.conn.commit()
        except sqlite3.Error:
            pass
    
    def update_value(self, column, value):
        query = f"UPDATE {TABLE} SET {column} = ? WHERE id = ?"
        self.cursor.execute(query, (f"{value}", self.guild.id))
        self.conn.commit()
        self._get_role()