class Author:
	def __init__(self,name):
		self.name = name

	def save(self,db):
		authors = self.find(db,self.name)
		if len(authors) > 0:
			return authors[0]['AUTHOR_ID']

		query = ("INSERT INTO AUTHOR "
			"(NAME) "
			"VALUES (\'%s\')" 
			%(self.name.replace("'","\\'")))
		return db.insert(query)

	def remove(self,db):
		query = ("DELETE FROM AUTHOR WHERE NAME=\'%s\'" %self.name.replace("'","\\'"))
		db.insert(query)	

	def find(self,db,name):
		query = ("SELECT * FROM AUTHOR WHERE NAME=\'%s\'" %name.replace("'","\\'"))
		return db.query(query)