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
        self.create_users_table()
    
    
    def create_database(self):
        self.cursor.execute("CREATE DATABASE goalmaster")


    def show_databases(self):
        databases = self.cursor.execute("SHOW DATABASES")
        for x in self.cursor:
            print(x)

    def create_users_table(self):
        """ create users table """
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                            (id int PRIMARY KEY AUTO_INCREMENT,
                            name varchar(255) NOT NULL, 
                            email varchar(255) NOT NULL UNIQUE, 
                            password varchar(255) NOT NULL)""")
        
    def create_goal(self, user_id, goal_name, goal_duration, goal_amount):
        """Create a goal for a specific user"""
        sql = "INSERT INTO goals (user_id, goal_name, goal_duration, goal_amount) VALUES (%s, %s, %s, %s)"
        values = (user_id, goal_name, goal_duration, goal_amount)
        self.cursor.execute(sql, values)
        self.db.commit()
        return True



    def create_user(self,name,email,password):
        password_bytes = bytes(password,'utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name,email,password_hash)
        execute = self.cursor.execute(sql,values)
        self.db.commit()
        return True
       
    def login(self,email,password):
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query,(email,))
        users = self.cursor.fetchall()
        for user in users:
            if bcrypt.checkpw(bytes(password,'utf-8'), bytes(user[-1],'utf-8')):
                return True
            else: 
                return False