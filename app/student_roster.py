#!/usr/bin/env python3
"""
The Student Roster data structure and its functions.
"""
from student import *
from os.path import exists

class StudentRoster:
	# Store the students in a set to be easily-retrievable?
	# Alternative: List or Dictionary?

	def __init__(self):
		self.students = set()
		try:
			with open("../student_data/roster.txt", "r") as f:
				self.lines = f.readlines()
		except FileNotFoundError:
			self.lines = []

	"""
	Creates a new roster from student data in the provided file.
	"""
	def import_roster_from_file(self, filename):
		try:
			file = open(filename, 'r')
		except (FileNotFoundError, IsADirectoryError):
			return "Unable to open file."
		try:
			self.lines = file.readlines()
		except UnicodeDecodeError:
			return "Invalid start byte. Are you sure this is a text file?"

		# Check the file format before parsing any data
		error = self.get_errors()
		if error :
			return error

		for line in self.lines:
			# Get rid of any whitespace and parse the fields per-line
			line = line.strip()
			fields = line.split("\t")

			# Read in the student's data from the roster file
			first = fields[0]
			last = fields[1]
			UO_ID = fields[2]
			email = fields[3]
			phonetic = fields[4]
			reveal_code = fields[5]

			# Create a new instance of the student class and add them to the roster
			student = Student(first, last, UO_ID, email, phonetic, reveal_code)
			self.add_student(student)
		return ""

	def save_internally(self):
		"""
		Write the lines of this roster to an internal file.
		"""
		with open("../student_data/roster.txt", "w") as internal_file:
			for line in self.lines:
				internal_file.write(line)

	def compare(self, other_roster):
		"""

		"""
		return self.students.symmetric_difference(other_roster.students)

	# TODO: LOAD FROM PICKLE ------------------
	"""
	def load_roster_from_pickle(self):
	"""
	
	# Potentially obsolete?
	def export_roster_to_file(self, directory):
		# TODO: MAKE SURE TO CHECK BEFORE OVERWRITING OLD DATA (AKA OLD SAVE FILE)

		path = f"{directory}/roster.txt"
		found = False
		i = 0
		while not found:
			if exists(path):
				path = f"{directory}/roster{i}.txt"
				i += 1
			else:
				found = True
		print("writing to", path)
		with open(path, "w") as f:
			for line in self.lines:
				f.write(line)
		return path

	def add_student(self, student):
		self.students.add(student)

	def remove_student(self, student):
		self.students.remove(student)

	# Returns the number of students in the current roster
	def num_students(self):
		return len(self.students)

	"""
	This function checks that a roster file is in the correct format
	Namely, it must contain the correct number of fields (6), and these
	fields must be of the correct types.
	"""
	def get_errors(self):
		for line in self.lines:
			line = line.strip()
			fields = line.split("\t")
			if len(fields) != 6:
				return ("Incorrect number of fields in the roster file. Each entry in the roster file should "
								"be formatted in the following manner: <first_name><tab><last_name><tab><UO "
								"ID><tab><email_address><tab><phonetic_spelling> <tab> <reveal_code> <LF>")
			else:
				UO_ID = fields[2]
				if len(UO_ID) != 9:
					return ("UO_IDs must be 9 digits long.")
				email_address = fields[3]
				""""  @uoregon.edujosh@gmail.com """
				if not (email_address.endswith("@uoregon.edu") or email_address.endswith("cs.uoregon.edu")):
					return "Incorrect email address format."
				reveal_code = fields[5]
				if not reveal_code.isdigit() or (int(reveal_code) != 0 and int(reveal_code) != 1):
					return "Reveal codes must be 0 for 'do not display' and 1 for 'permission to display.'"
		return ""
