class Publication:
	def __init__(self,pub_id):
		self.id = pub_id
		self.year = 0
		self.title = ""
		self.abstract = ""
		self.venue = ""

	def save(self,db):
		query = ("INSERT INTO PUBLICATION "
			"(PUB_ID, YEAR, TITLE, ABSTRACT, VENUE) "
			"VALUES (%s,%d,\"%s\",\"%s\",\"%s\")" 
			%(self.id,self.year,self.title,self.abstract,self.venue))
		db.insert(query)

	def remove(self,db):
		query = ("DELETE FROM PUBLICATION WHERE PUB_ID=%s" %self.id)
		db.insert(query)

	def exists(self,db):
		query = ("SELECT PUB_ID FROM PUBLICATION WHERE PUB_ID=%s" %self.id)
		return len(db.query(query)) > 0
