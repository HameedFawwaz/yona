import os
import sqlite3

DATABASE = os.getcwd()+'/databases/welcome.db'
TABLE = "Guilds"

class WelcomeDB:
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
        self._get_welcome_message()

    def close(self):
        self.conn.close()
        del self

    def _create_table(self):
        query = f"""CREATE TABLE IF NOT EXISTS {TABLE} (id BIGINT, channel BIGINT, message TEXT)"""
        self.cursor.execute(query)
        self.conn.commit()

    def _get_welcome_message(self):
        query = f"SELECT * FROM {TABLE} WHERE id = ?"
        self.cursor.execute(query, (self.guild.id,))
        info = self.cursor.fetchall()
        if info:
            self.welcome_message = info[0][2]
            return self.welcome_message
        else:
            self._create_new_welcome()
            self._get_welcome_message()
    
    def _get_welcome_channel(self):
        query = f"SELECT * FROM {TABLE} WHERE id = ?"
        self.cursor.execute(query, (self.guild.id,))
        info = self.cursor.fetchall()
        if info:
            self.channel = info[0][1]
            return self.channel
        else:
            self._create_new_welcome()
            self._get_welcome_channel()

    def _create_new_welcome(self):
        try:
            query = f"""INSERT INTO {TABLE} VALUES (?, ?, ?)"""
            self.cursor.execute(query, (self.guild.id, None, ''))
            self.conn.commit()
        except sqlite3.Error:
            pass
    
    def update_value(self, column, value):
        query = f"UPDATE {TABLE} SET {column} = ? WHERE id = ?"
        self.cursor.execute(query, (f"{value}", self.guild.id))
        self.conn.commit()
        self._get_welcome_message()