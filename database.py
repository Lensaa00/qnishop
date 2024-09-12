import sqlite3

from aiohttp import request


class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    # USER FUNCTIONS
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
        r = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return r

    def get_user_referrals(self, user_id):
        r = self.cursor.execute("SELECT * FROM users WHERE referral_id = ?", (user_id,)).fetchall()
        return len(r)

    def get_user_balance(self, user_id):
        r = self.cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return r[0]

    def update_user_balance(self, user_id, balance):
        self.cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id,))
        self.connection.commit()

    def update_user_admin(self, user_id):
        is_user_admin = self.user_admin(user_id)
        is_user_admin = int(not is_user_admin)
        self.cursor.execute("UPDATE users SET is_admin = ? WHERE user_id = ?", (user_id, is_user_admin,))
        self.connection.commit()

    def user_admin(self, user_id):
        r = self.cursor.execute("SELECT is_admin FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return bool(int(r[0]))

    # CATEGORIES FUNCTIONS
    def get_categories(self):
        return self.cursor.execute("SELECT * FROM categories").fetchall()

    # ITEMS FUNCTIONS
    def get_items_by_category(self, category_id):
        return self.cursor.execute("SELECT * FROM items WHERE category = ?", (category_id,)).fetchall()