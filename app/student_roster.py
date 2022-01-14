#!/usr/bin/env python3
"""
The Student Roster data structure and its functions.
"""
from student import*

class StudentRoster:
	# Store the students in a set to be easily-retrievable?
	# Alternative: List or Dictionary?
	student_list = set()

	def __init__(self):
		student_list = set()

	"""
	Creates a new roster from student data in the provided file.
	"""
	def import_roster_from_file(self, filename):
		# TODO: MAKE SURE TO CHECK BEFORE OVERWRITING OLD DATA ^^^
		file = open(filename)
		lines = file.readlines()

		# Check the file format before parsing any data
		if not self.correct_file_format(lines):
			raise ValueError

		for line in lines:
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
	
	# TODO: LOAD FROM PICKLE ------------------
	"""
	def load_roster_from_pickle(self):
	"""
	
	# Potentially obsolete?
	def export_roster_to_file(self):
		# TODO: MAKE SURE TO CHECK BEFORE OVERWRITING OLD DATA (AKA OLD SAVE FILE)
		f = open("roster_export.txt", "w")

		for student in self.student_list:
			f.write(student.first_name + "\t")
			f.write(student.last_name + "\t")
			f.write(student.UO_ID + "\t")
			f.write(student.email_address + "\t")
			f.write(student.phonetic_spelling + "\t")
			f.write(student.reveal_code + "\t")

	def add_student(self, student):
		self.student_list.add(student)

	def remove_student(self, student):
		self.student_list.remove(student)

	# Returns the number of students in the current roster
	def num_students(self):
		return len(self.student_list)

	"""
	This function checks that a roster file is in the correct format
	Namely, it must contain the correct number of fields (6), and these
	fields must be of the correct types.
	"""
	def correct_file_format(self, lines):
		for line in lines:
			line = line.strip()
			fields = line.split("\t")
			if len(fields) != 6:
				raise ValueError("Incorrect number of fields in the roster file. Each entry in the roster file should "
								"be formatted in the following manner: <first_name><tab><last_name><tab><UO "
								"ID><tab><email_address><tab><phonetic_spelling> <tab> <reveal_code> <LF>")
			else:
				UO_ID = fields[2]
				if len(UO_ID) != 9:
					raise ValueError("UO_IDs must be 9 digits long.")
				email_address = fields[3]
				""""  @uoregon.edujosh@gmail.com """
				if not (email_address.endswith("@uoregon.edu") or email_address.endswith("cs.uoregon.edu")):
					raise ValueError("Incorrect email address format.")
				reveal_code = fields[5]
				if not reveal_code.isdigit() or (int(reveal_code) != 0 and int(reveal_code) != 1):
					raise ValueError("Reveal codes must be 0 for 'do not display' and 1 for 'permission to display.'")
		return True
