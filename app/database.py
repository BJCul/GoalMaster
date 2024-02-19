import mysql.connector
import datetime

class MySQLdb:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="softballpersons0123",
            database="goalmaster"
            )
        self.cursor = self.db.cursor()
        self.create_user_table()        
        self.create_goal_table()
        self.create_expenses()
        self.create_savings()

    def create_user_table(self):
        """Create the user table"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                            (id     integer         AUTO_INCREMENT PRIMARY KEY, 
                            name    varchar(255)    NOT NULL,
                            password varchar(50)    NOT NULL,
                            email   varchar(255)    NOT NULL,             
                            loggedin BOOLEAN        NOT NULL CHECK (loggedin IN (0, 1)), 
                            keeploggedin BOOLEAN    NOT NULL CHECK (keeploggedin IN (0, 1)))""")
        self.db.commit()
    
    def create_user(self, name, email, password, keeploggedin=0):
        """Create a user"""
        sql = "INSERT INTO users(name, email, password, loggedin, keeploggedin) VALUES(%s, %s, %s, %s, %s)"
        values = (name, email, password, 0, keeploggedin)
        self.cursor.execute(sql, values)
        self.db.commit()
        print(self.cursor.rowcount, "record inserted.")

    def check_email(self, email):
        """Check to see if the email already exists in the database before going onto creating a user"""
        self.cursor.execute("SELECT id, email FROM users WHERE email = %s", (email,))
        the_user = self.cursor.fetchall()
        if not the_user:
            return False
        else:
            return True
            
    def get_user(self, email, password, keepmelogged):
        """Get the user when logging in to the system"""
        self.cursor.execute("SELECT id, email, name FROM users WHERE email = %s AND password = %s", (email, password))
        user_id = self.cursor.fetchall()
        if user_id:
            self.cursor.execute("UPDATE users SET loggedin = 0 WHERE loggedin = 1")
            if keepmelogged:
                self.cursor.execute("UPDATE users SET loggedin = 1, keeploggedin = 1 WHERE id = %s", (user_id[0][0],))
            else:
                self.cursor.execute("UPDATE users SET loggedin = 1 WHERE id = %s", (user_id[0][0],))

            self.db.commit()
            return True, user_id[0][0]
        else:
            return False, None


    def get_users(self, email, password, keepmelogged):
        """Get the user when logging in to the system"""
        self.cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
        user_id = self.cursor.fetchall()
        if user_id:
            self.cursor.execute("UPDATE users SET loggedin = 0 WHERE loggedin = 1")
            if keepmelogged:
                self.cursor.execute("UPDATE users SET loggedin = 1, keeploggedin = 1 WHERE id = %s", (user_id[0][0],))
            else:
                self.cursor.execute("UPDATE users SET loggedin = 1 WHERE id = %s", (user_id[0][0],))

            self.db.commit()
            return user_id[0][0], True
        else:
            return False
        
    def get_users_info(self, user_id):
        try:           
            self.cursor.execute("SELECT name, email FROM users WHERE id=%s", (user_id,))
            users_info = self.cursor.fetchall()
            if users_info:  # Check if there are users
                return users_info  # Return the users_info
            else:
                print("No users found for with user ID:", user_id)
                return None
        except Exception as e:
            print("Error fetching users:", e)
            return None

    def change_account_name(self, user_id, new_name):
        try:
            # Execute the SQL query to update the name
            self.cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, user_id))
            self.db.commit()            
            # Retrieve the updated name from the database
            self.cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
            updated_name = self.cursor.fetchone()[0]  # Fetch the first column of the first row
            return updated_name
        except Exception as e:
            print("Error updating name:", e)
            self.db.rollback()

    def change_account_email(self, user_id, new_email):
        try:
            self.cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, user_id))
            self.db.commit()
            self.cursor.execute("SELECT email FROM users WHERE id = %s", (user_id,))
            updated_email = self.cursor.fetchone()[0]  # Fetch the first column of the first row
            return updated_email
        except Exception as e:
            print("Error updating email:", e)
            self.db.rollback()

    def change_account_password(self, user_id, new_password):
        try:
            self.cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
            self.db.commit()
        except Exception as e:
            print("Error updating password:", e)
            self.db.rollback()

    
    def get_logged_in_user_email(self):
        """Get the email of the currently logged in user"""
        self.cursor.execute("SELECT email FROM users WHERE loggedin = 1")
        email = self.cursor.fetchall()
        if email:
            return email[0][0]
        else:
            return None
    
    def get_logged_in_userid(self):
        """Get the userid of the currently logged in user"""
        self.cursor.execute("SELECT id FROM users WHERE loggedin = 1")
        userid = self.cursor.fetchall()
        if userid:
            return userid[0][0]
        else:
            return None

    def get_keep_logged_in(self):
        '''Check if there is any user with keepmelogged = 1'''
        self.cursor.execute("SELECT * FROM users WHERE keeploggedin = 1")
        logged = self.cursor.fetchall()
        if logged:
            return True
        else:
            return False

    def log_out_user(self):
        """Triggered when the user logsout"""
        self.cursor.execute("UPDATE users SET loggedin = 0, keeploggedin = 0 WHERE loggedin = 1")
        self.db.commit()
        return True
    #####################################FOR GOAL#####################################
    def create_goal_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS goals
                    (goal_id             INT     PRIMARY KEY AUTO_INCREMENT,
                    user_id         INT,         
                    goal_name       varchar(255)         NOT NULL,
                    goal_amount     DECIMAL(10,2)        NOT NULL,
                    goal_duration   DATE,
                    allowance       DECIMAL(10,2)        NOT NULL,
                    creation_date       DATE,
                    FOREIGN KEY (user_id) REFERENCES users(id))""")

    
    def create_goals(self,user_id,goal_name, goal_amount, goal_duration, allowance):
        sql = "INSERT INTO goals (user_id, goal_name, goal_amount, goal_duration, allowance) VALUES (%s, %s, %s,%s, %s)"
        values = (user_id,goal_name, goal_amount, goal_duration, allowance)
        try:
            self.cursor.execute (sql, values)
            self.db.commit()
            return user_id,goal_name, goal_amount, goal_duration, allowance

        except Exception as e:
            print("Error creating goal:", e) 
    
    def get_goal_id(self, user_id):
        try:           
            """Get the goal_id of the currently logged in user"""
            self.cursor.execute("SELECT goal_id FROM goals WHERE user_id=%s", (user_id,))
            goalid = self.cursor.fetchone()
            if goalid:
                return goalid[0]
            else:
                return None            
            
        except Exception as e:
            print("Error fetching goals:", e)
            return None
    
    def get_goal_id_(self, user_id):
        try:           
            """Get the goal_id of the currently logged in user"""
            self.cursor.execute("SELECT goal_id FROM goals WHERE user_id=%s ORDER BY goal_id DESC LIMIT 1", (user_id,))
            goalid = self.cursor.fetchall()
            if goalid:
                return goalid[0][0]
            else:
                return None            
            
        except Exception as e:
            print("Error fetching goals:", e)
            return None
        
    def get_goals(self, user_id):
        try:           
            self.cursor.execute("SELECT * FROM goals WHERE user_id=%s ORDER BY goal_id DESC LIMIT 1", (user_id,))
            goals = self.cursor.fetchone()
            self.db.commit()
            if goals:  # Check if there are goal
                return goals
            else:
                print("No goals found for with user ID:", user_id)
                return None
            
        except Exception as e:
            print("Error fetching goals:", e)
            return None
        
    def get_allowance(self, goal_id):
        try:           
            self.cursor.execute("SELECT allowance FROM goals WHERE goal_id=%s", (goal_id,))
            allowance = self.cursor.fetchall()
            self.db.commit()
            if allowance:  # Check if there are goal
                return allowance  # Return the first goal
            else:
                print("No goals found for with user ID:", goal_id)
                return None

        except Exception as e:
            print("Error fetching goals:", e)
            return None  
    #####################################FOR SAVINGS#############################################
    def create_savings(self):  
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS savings (
                                savings_id INT AUTO_INCREMENT PRIMARY KEY,
                                goal_id INT,
                                creation_date DATE,
                                savings_amount DECIMAL(10, 2),                                
                                FOREIGN KEY (goal_id) REFERENCES goals(goal_id)
                                );
                                """)

    def add_leftover_to_savings(self, user_id, leftover_amount):
        try:
            # Insert leftover amount into savings table
            current_date = datetime.datetime.now().date()
            sql = "INSERT INTO savings (user_id, amount, date_saved) VALUES (%s, %s, %s)"
            values = (user_id, leftover_amount, current_date)
            self.cursor.execute(sql, values)
            self.db.commit()
            print("Leftover added to savings successfully!")
        except Exception as e:
            print("Error adding leftover to savings:", e)
            self.db.rollback()

    def update_savings_from_allowance(self, user_id, daily_allowance):
        # Calculate leftover allowance
        leftover_amount = self.calculate_leftover_allowance(user_id, daily_allowance)

        # Add leftover amount to savings if positive
        if leftover_amount > 0:
            self.add_leftover_to_savings(user_id, leftover_amount)

    def calculate_leftover_allowance(self, user_id, daily_allowance):
        try:
            # Calculate total expenses for the day
            today = datetime.datetime.now().date()
            total_expenses = self.get_total_expenses_for_day(user_id, today)

            # Calculate leftover allowance
            leftover_allowance = daily_allowance - total_expenses
            return max(leftover_allowance, 0)  # Ensure leftover is non-negative
        except Exception as e:
            print("Error calculating leftover allowance:", e)
            return

    def get_total_expenses_for_day(self, user_id, date):
        try:
            # Convert date to string in YYYY-MM-DD format
            date_str = date.strftime('%Y-%m-%d')

            # Query to get total expenses for the user on the given date
            sql = "SELECT SUM(expense_amount) FROM expenses WHERE user_id = %s AND DATE(expense_date) = %s"
            values = (user_id, date_str)
            self.cursor.execute(sql, values)

            # Fetch the result
            total_expenses = self.cursor.fetchone()[0]  # Total expenses will be the first (and only) column in the result

            # If there are no expenses for the day, return 0
            if total_expenses is None:
                return 0

            return total_expenses
        except Exception as e:
            print("Error fetching total expenses for the day:", e)
            return 0  # Return 0 in case of an error
        
            
    #####################################FOR EXPENSES######################################

    def create_expenses(self):  
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
                                expenses_id INT AUTO_INCREMENT PRIMARY KEY,
                                goal_id INT,
                                expense_name VARCHAR(255),
                                expense_date DATE,
                                expense_amount DECIMAL(10, 2),                                
                                FOREIGN KEY (goal_id) REFERENCES goals(goal_id)
                                );
                                """)
        self.db.commit()
    
    def insert_expenses(self, goal_id, expense_name, expense_amount):
        try:
            sql = "INSERT INTO expenses (goal_id, expense_name, expense_amount) VALUES (%s, %s, %s)"
            values = (goal_id, expense_name, expense_amount)
            self.cursor.execute (sql, values)
            self.db.commit()
            self.cursor.fetchall()  
            return True
        
        except Exception as e:
            # Handle any exceptions that occur during the insertion process
            self.db.rollback()  # Rollback the transaction in case of an error
            print("Error inserting expense:", e)
         
    def delete_expenses(self, expenses_id):
        sql = "DELETE FROM expenses WHERE expenses_id=%s"
        value = (expenses_id,)
        self.cursor.execute (sql, value)
        self.db.commit()
        return True 


    def get_expenses(self, goal_id):
        try:           
            self.cursor.execute("SELECT * FROM expenses WHERE goal_id=%s", (goal_id,))
            expenses = self.cursor.fetchall()
            self.db.commit()
            if expenses:  
                return expenses  
            else:
                return None
            
        except Exception as e:
            print("Error fetching expenses:", e)
            return None


    
    def total_spending(self, goal_id):
        try:
            self.cursor.execute("SELECT SUM(expense_amount) FROM expenses WHERE goal_id = %s", (goal_id,))
            total_expenses = self.cursor.fetchall()
            return total_expenses if total_expenses is not None else 0  
        except Exception as e:
            print("Error fetching total expenses:", e)
            return 0 



    def close_db_connection(self):
        self.cursor.close()
    