# db/database.py
import sqlite3

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        # Create tables for goals and expenses
        self.conn.execute('''CREATE TABLE IF NOT EXISTS goals (
                             id INTEGER PRIMARY KEY,
                             name TEXT,
                             target_amount REAL,
                             duration INTEGER,
                             start_date TEXT,
                             daily_savings REAL
                             )''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
                             id INTEGER PRIMARY KEY,
                             goal_id INTEGER,
                             amount REAL,
                             date TEXT,
                             description TEXT,
                             FOREIGN KEY(goal_id) REFERENCES goals(id)
                             )''')
        self.conn.commit()

    # Add methods for adding, updating, and querying data
    # For example, add_goal, update_goal, get_goals, add_expense, etc.

    def close(self):
        self.conn.close()
