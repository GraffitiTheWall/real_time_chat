import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'H2g9gD8U#%r%',
    database = 'users'
)

cursor = mydb.cursor()

class SQLCursor : 
    def __init__(self) : 
        self.cursor = mydb.cursor()
    def get_last_id(self,table) : 
        query = f"SELECT user_id FROM {table} ORDER BY user_id DESC LIMIT 1;"
        self.cursor.execute(query)
        return [data[0] for data in self.cursor][0]
    def insert_comment(self, user_name,user_comment,time_created) : 
        user_comment = user_comment.replace('"',"''")
        user_name = user_name.replace('"',"''")
        next_id = self.get_last_id('user_comment_info') + 1
        query = f'INSERT INTO user_comment_info(user_id,user_name,user_comment,time_created) VALUES({next_id},"{user_name}", "{user_comment}","{time_created}")'
        self.cursor.execute(query)
        mydb.commit()
    def get_all_comments(self) : 
        query = "SELECT user_name, user_comment,time_created FROM user_comment_info;"
        self.cursor.execute(query)
        lst = [list(data) for data in self.cursor]
        return lst