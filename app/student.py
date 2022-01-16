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

	def __members(self):
		# The __members, __eq__, and __hash__ methods are based on code by Jonas Adler (2007)
		# published as a Stack Overflow answer here: https://stackoverflow.com/questions/45164691/recommended-way-to-implement-eq-and-hash
		# Since the total_num_flags and dates_called are mutable, we don't want
		# to use them for the hash. The other pieces of data are not changed.
		# We also don't use the student ID in the hash, per project specifications.

		return (self.first_name, self.last_name, self.email_address, self.phonetic_spelling, self.reveal_code)

	def __hash__(self):
		return hash(self.__members())

	def __eq__(self, other):
		# TODO: should student ID be used in checking for equqlity? Currently it's not.
		return isinstance(other, Student) and self.__members() == other.__members()


