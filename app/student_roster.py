#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Student Roster Class

Description:    The Student Roster Class for the CoolCall Program.
                This module is responsible for reading in a Student Roster from
                a user-provided data file, converting the read data into
                Student objects.

Authors:        EnterPrize Labs:
                Arden Butterfield, Madison Werries, Amy Reichold,
                Quinn Fetrow, and Derek Martin

Last Edited:    1/23/2022
Last Edit By:   Madison Werries
"""
###############################################################################
from student import *
from os.path import exists
from constants import *
###############################################################################

class StudentRoster:
	""" A class to represent all the students currently in a course.

		Attributes
		=======================================================================
		students
			a list of Student objects
		lines
			the lines read in from the roster txt file
		
		Methods
		=======================================================================
		import_roster_from_file(filename)
			Creates a new roster from student data in the provided file.
		save_internally()
			Saves the data in the roster to an internal file.
		compare()
			Compares the contents of two rosters, returning the differences.
		export_roster_to_file(directory)
			Exports the roster to a file in the specified directory.
		add_student(student)
			Adds the specified student to the queue.
		remove_student(student)
			Removes the specified student from the queue.
		num_students()
			Returns the number of students currently in the queue.
		get_errors()
			Returns any errors with the format of a provided roster file.
	"""
	
	def __init__(self):
		""" Constructs an empty student roster object. """
		self.students = set()
		try:
			with open("../input_data/roster.txt", "r") as f:
				self.lines = f.readlines()
		except FileNotFoundError:
			self.lines = []

	def import_roster_from_file(self, filename):
		""" Creates a new roster from student data in the provided file. """
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
		if error:
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
		""" Saves the data in the roster to an internal file. """
		with open("../student_data/roster.txt", "w") as internal_file:
			for line in self.lines:
				internal_file.write(line)

	def compare(self, other_roster):
		""" Compares the contents of two rosters, returning the differences. """
		#return self.students.symmetric_difference(other_roster.students)

	def export_roster_to_file(self, directory):
		""" Exports the roster to a file in the specified directory. """
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
		""" Adds the specified student to the queue. """
		self.students.add(student)

	def remove_student(self, student):
		""" Removes the specified student from the queue. """
		self.students.remove(student)

	def num_students(self):
		""" Returns the number of students currently in the queue. """
		return len(self.students)

	def get_errors(self):
		""" This function checks that a roster file is in the correct format.
		Namely, it must contain the correct number of fields (6), and that
		these fields are of the correct type and/or format. """
		for line in self.lines:
			line = line.strip()
			fields = line.split(ROSTER_DELIMITER)
			if len(fields) != 6:
				return ("Incorrect number of fields in the roster file. Each entry in the roster file should "
								"be formatted in the following manner: <first_name><delimiter><last_name><delimiter><UO "
								"ID><delimiter><email_address><delimiter><phonetic_spelling><delimiter><reveal_code><LF>")
			else:
				UO_ID = fields[2]
				if len(UO_ID) != 9:
					return "UO IDs must be 9 digits long."
				if not UO_ID.isnumeric():
					return "UO IDs must only contain digits"
				email_address = fields[3]
				""""  @uoregon.edujosh@gmail.com """
				if not (email_address.endswith("@uoregon.edu") or email_address.endswith("cs.uoregon.edu")):
					return "Incorrect email address format."
				reveal_code = fields[5]
				if not reveal_code.isdigit() or (int(reveal_code) != 0 and int(reveal_code) != 1):
					return "Reveal codes must be 0 for 'do not display' and 1 for 'permission to display.'"
		return ""
