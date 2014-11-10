class AuthorPub:
	def __init__(self,au_id,pub_id):
		self.au_id = au_id
		self.pub_id = pub_id

	def save(self,db):
		query = ("INSERT INTO AUTHOR_PUB "
			"(AUTHOR_ID,PUB_ID) "
			"VALUES (%s,%s)" 
			%(self.au_id,self.pub_id))
		return db.insert(query)

	def find_by_author(self,db,au_id):
		query = ("SELECT * FROM AUTHOR_PUB WHERE AUTHOR_ID=%s" %au_id)
		return db.query(query)	

	def find_by_publication(self,db,pub_id):
		query = ("SELECT * FROM AUTHOR_PUB WHERE PUB_ID=%s" %pub_id)
		return db.query(query)