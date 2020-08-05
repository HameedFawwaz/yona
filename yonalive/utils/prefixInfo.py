import os
import sqlite3

DATABASE = os.getcwd()+'/databases/prefix.db'
TABLE = "Prefixes"

class PrefixDB:
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
        self._get_prefix()

    def close(self):
        self.conn.close()
        del self

    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE} (g_id BIGINT, prefix TEXT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def _get_prefix(self):
        query = f"SELECT * FROM {TABLE} WHERE g_id = ?"
        self.cursor.execute(query, (self.guild.id,))
        info = self.cursor.fetchall()
        if info:
            self.prefix = info[0][1]
            return self.prefix
        else:
            self._create_new_prefix()
            self._get_prefix()


    def _create_new_prefix(self):
        try:
            query = f"""INSERT INTO {TABLE} VALUES (?, ?)"""
            self.cursor.execute(query, (self.guild.id, "y-"))
            self.conn.commit()
        except sqlite3.Error:
            pass
    
    def update_value(self, column, pre):
        query = f"UPDATE {TABLE} SET {column} = ? WHERE g_id = ?"
        self.cursor.execute(query, (pre, self.guild.id))
        self.conn.commit()
        self._get_prefix()