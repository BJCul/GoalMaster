import mysql.connector
import bcrypt

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
        self.show_table()

    def show_db(self):
        """show database"""
        self.cursor.execute("show databases")
        for x in self.cursor:
            print(x)
    
    def show_table(self):
        """show table"""
        self.cursor.execute("show tables")
        for x in self.cursor:
            print(x)

    def create_user_table(self):
        """Create the user table"""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                            (id integer AUTO_INCREMENT PRIMARY KEY, 
                            name varchar(255) NOT NULL,
                            password varchar(50) NOT NULL,
                            email varchar(255) NOT NULL,             
                            loggedin BOOLEAN NOT NULL CHECK (loggedin IN (0, 1)), 
                            keeploggedin BOOLEAN NOT NULL CHECK (keeploggedin IN (0, 1)))""")
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
        self.cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
        user_id = self.cursor.fetchall()
        if user_id:
            self.cursor.execute("UPDATE users SET loggedin = 0 WHERE loggedin = 1")
            if keepmelogged:
                self.cursor.execute("UPDATE users SET loggedin = 1, keeploggedin = 1 WHERE id = %s", (user_id[0][0],))
            else:
                self.cursor.execute("UPDATE users SET loggedin = 1 WHERE id = %s", (user_id[0][0],))

            self.db.commit()
            return True
        else:
            return False

    
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
            return False
        else:
            return True

    def log_out_user(self):
        """Triggered when the user logsout"""
        self.cursor.execute("UPDATE users SET loggedin = 0, keeploggedin = 0 WHERE loggedin = 1")
        self.db.commit()
    
    def close_db_connection(self):
        self.cursor.close()
    
