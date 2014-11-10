class Citation:
	def __init__(self,pub_id,ref_id):
		self.pub_id = pub_id
		self.ref_id = ref_id

	def save(self,db):
		query = ("INSERT INTO CITATION "
			"(PUB_ID,REF_ID) "
			"VALUES (%s,%s)" 
			%(self.pub_id,self.ref_id))
		return db.insert(query)

	def find_by_reference(self,db,ref_id):
		query = ("SELECT * FROM CITATION WHERE REF_ID=%s" %ref_id)
		return db.query(query)	

	def find_by_publication(self,db,pub_id):
		query = ("SELECT * FROM CITATION WHERE PUB_ID=%s" %pub_id)
		return db.query(query)	