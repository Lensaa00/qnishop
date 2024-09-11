import sqlite3

from aiohttp import request


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        return self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def create_user(self, user_id, user_name):
        self.cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name,))
        self.connection.commit()

    def create_user_referral(self, user_id, user_name, referral_id):
        self.cursor.execute("INSERT INTO users (user_id, user_name, referral_id) VALUES (?, ?, ?)",
                            (user_id, user_name, referral_id,))
        self.connection.commit()

    def get_user(self, user_id):
        request = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return request

    def get_user_referrals(self, user_id):
        request = self.cursor.execute("SELECT * FROM users WHERE referral_id = ?", (user_id,)).fetchall()
        return len(request)

    def get_user_balance(self, user_id):
        request = self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return request[0]

    def update_user_balance(self, user_id, balance):
        self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))
        self.connection.commit()
