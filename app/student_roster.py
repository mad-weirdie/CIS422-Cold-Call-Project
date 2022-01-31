#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Student Roster Class

Description:    The Student Roster Class for the CoolCall Program.
                This module is responsible for reading in a Student Roster from
                a user-provided data file, converting the read data into
                Student objects.

Authors:        Arden Butterfield, Quinn Fetrow, Derek Martin, Amy Reichhold,
			    Madison Werries 

Last Edited:    1/30/2022
Last Edit By:   Madison Werries
"""
###############################################################################
from student import Student
from os.path import exists
from constants import *
###############################################################################

class StudentRoster:
	""" 
	A class to represent all the students currently enrolled in a course.

		Attributes
		=======================================================================
		students
			a list of Student objects
		lines
			the lines read in from the roster txt file
		
		Methods
		=======================================================================
		import_roster_from_file(filename)
			Creates a new roster from student data in the specified file.
		save_internally()
			Saves the roster data to an internal file.
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
	
	# Constructs an empty student roster object.
	def __init__(self):
		self.students = set()
		try:
			with open(INTERNAL_ROSTER_LOCATION, "r") as f:
				self.lines = f.readlines()
		except FileNotFoundError:
			self.lines = []

	def import_roster_from_file(self, filename):
		"""
		Creates a new roster from student data in the specified file.
		If not possible, return a descriptive error.

		filename: (string) The file path of the roster we want to import.
		returns: (string) a descriptive error, or an empty string if the
		import is successful.
		"""
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

		# The first line of the roster file is a comment, and so is not parsed
		# when reading in student data.
		for line in self.lines[1:]:
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
		Saves the roster data to an internal file. 
		"""
		with open(INTERNAL_ROSTER_LOCATION, "w") as internal_file:
			for line in self.lines:
				internal_file.write(line)

	def compare(self, other_roster):
		""" 
		Compares the contents of two rosters.

		other_roster: (Roster) a separate roster to compare with self
		returns: a set of student objects that are present in one roster
		but not in the other. 
		
		(NOTE -- the "same student" might be returned twice by this function. 
		For example, if we change the email address of a student between two rosters
		and then compare them, it will return the student twice in the set: 
		Once with the old email address, and once with the new email address)
		"""
		return self.students.symmetric_difference(other_roster.students)

	def export_roster_to_file(self, directory):
		""" 
		Exports the roster to a file, called roster.txt or roster<i>.txt,
		in the specified directory.

		directory: (string)
		returns: (string) the path of the specified directory
		"""
		path = self._get_path_name(directory)
		with open(path, "w") as f:
			for line in self.lines:
				f.write(line)
		return path

	def _get_path_name(self, directory):
		"""
		To avoid overwriting data, we want to find an unused filename to
		save the roster to. Ideally, it should be <directory>/roster.txt.
		If that is unavailable, it should be <directory>/roster<i>.txt for
		the smallest possible natural number <i>

		directory: (string)
		returns: (string) the path of the specified directory
		"""
		path = f"{directory}/roster.txt"
		found = False
		i = 0
		while not found:
			if exists(path):
				path = f"{directory}/roster{i}.txt"
				i += 1
			else:
				found = True
		return path

	def add_student(self, student):
		"""
		Add the specified Student object to the roster.

		student: (Student)
		"""
		self.students.add(student)

	def remove_student(self, student):
		"""
		Remove the specified Student object from the roster.

		student: (Student)
		returns: (boolen) True if the student is found in the roster, False otherwise.
		"""
		if student in self.students:
			self.students.remove(student)
			return True
		return False

	def num_students(self):
		""" 
		returns: (int) the number of students currently in the roster. 
		"""
		return len(self.students)

	def get_errors(self):
		""" 
		This function checks that a roster file is in the correct format.
		Namely, it must contain the correct number of fields (6). 
		The function checks that these fields are of the correct type and/or format. 

		returns: (string) a descriptive error message, or an empty string
		"""
		# The first line of the roster file is a comment, and so is not parsed
		# when reading in student data.
		for line in self.lines[1:]:
			# Each line is separated by a line-feed character, which is not part
			# of any data field
			line = line.strip()
			# The data fields are separated by a character (tab by default)
			# specified in the constants file.
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
				if not reveal_code.isdigit():
					return "Reveal codes must be 0 for 'display', or any other value for 'do not display'"
		return ""
