"""
Student data structure: Holds per-student roster data.
"""

class Student:
	# List of standard attributes
	first_name = ""
	last_name = ""
	UO_ID = "95xxxxxxx"
	email_address = ""
	phonetic_spelling = ""
	reveal_code = ""
	total_num_flags = 0

	"""
	Constructor for the Student class.
	Alternatively, it could accepts a string read from roster
	file to be parsed within the function?
	"""
	def __init__(self, fname, lname, sid, email, phonetic, rcode):
		self.first_name = fname
		self.last_name = lname
		self.UO_ID = sid
		self.email_address = email
		self.phonetic_spelling = phonetic
		self.reveal_code = rcode
		self.total_num_flags = 0

