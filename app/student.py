"""
Student data structure: Holds per-student roster data.
"""
from datetime import date

class Student:
	# List of standard attributes
	first_name = ""
	last_name = ""
	UO_ID = "95xxxxxxx"
	email_address = ""
	phonetic_spelling = ""
	reveal_code = ""
	total_num_flags = 0
	dates_called = []
	"""
	Constructor for the Student class. Alternatively, it could accepts a string
	read from roster file to be parsed within the function?
	"""
	def __init__(self, fname, lname, sid, email, phonetic, rcode):
		self.first_name = fname
		self.last_name = lname
		self.UO_ID = sid
		self.email_address = email
		self.phonetic_spelling = phonetic
		self.reveal_code = rcode
		self.total_num_flags = 0
		self.dates_called = []
		
	def call_on(self, flag):
		if(flag):
			self.total_num_flags = self.total_num_flags + 1
		self.dates_called.append(date.today())
	
	def get_name(self):
		return self.first_name + " " + self.last_name
