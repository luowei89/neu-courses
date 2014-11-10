import MySQLdb

class Database:
    host = 'localhost'
    user = 'root'
    password = ''
    db = 'AP_DATA'
    def __init__(self):
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.db,charset='utf8')
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()
        return self.cursor.lastrowid

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

if __name__ == '__main__':
	db = Database()
	db.insert("")