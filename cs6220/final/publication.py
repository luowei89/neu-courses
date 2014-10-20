
class Publication:
	def __init__(self,pub_id):
		self.id = pub_id
		self.authors = []
		self.cited = 0
		self.year = 0
		self.title = ""
		self.abstract = ""
		self.venue = ""

	def add_cites(self):
		self.cited += 1