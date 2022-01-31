#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Student Class

Description:    The Student Class for the CoolCall Program.
                This module stores data about an individual student, and keeps
                track of when they have been called on.

Authors:        Arden Butterfield, Quinn Fetrow, Madison Werries

Last Edited:    1/25/2022
Last Edit By:   Arden Butterfield
"""
###############################################################################
from datetime import date
###############################################################################

class Student:
	"""
	A class to represent a single student in a course.
	
	Attributes
	============================================================================
	first_name, last_name, UO_ID, email_address, phonetic_spelling
		The corresponding information about the student, stored as a string

	reveal_code
		If the student will be included on-deck. 0 means the student will be
		included, another number means the student will not be included.

	total_num_flags
		The number of times a student has "flagged" when called on.

	dates_called
		A list of datetime objects, one for each date/time that a student has 
		been cold called..

	Methods
	============================================================================
	call_on(flag)
		Records that the student was called on during the current day, and
		increments the number of times the student has been called on (with a
		flag if flagged=True).

	get_name()
		Returns a formatted string of the student

	include_on_deck()
		Returns a boolean: is this student marked to be included on-deck?

	This class supports comparison for equality, and can be hashed to use in a
	Python set.
	"""

	def __init__(self, fname, lname, sid, email, phonetic, rcode):
		""" All fields should be passed in as strings."""
		self.first_name = fname
		self.last_name = lname
		self.UO_ID = sid
		self.email_address = email
		self.phonetic_spelling = phonetic
		self.reveal_code = rcode
		self.total_num_flags = 0
		self.dates_called = []
		
	def call_on(self, flag):
		"""
		Stores a new instance of the student being called on. 
		This method adds the current date to the list of dates called, 
		and increments the number of times that student has been called on 
		(with a flag, if applicable).

		flag: (boolen)
		"""
		if(flag):
			self.total_num_flags += 1
		self.dates_called.append(date.today())
	
	def get_name(self):
		""" 
		Returns a formatted string of the student
		"""
		return self.first_name + " " + self.last_name

	def include_on_deck(self):
		# We may not want to include some students in the cold calling display,
		# as communicated by the reveal code.
		return self.reveal_code == "0"

	def __members(self):
		# The __members, __eq__, and __hash__ methods are based on code by Jonas Adler (2007)
		# published as a Stack Overflow answer here:
		# https://stackoverflow.com/questions/45164691/recommended-way-to-implement-eq-and-hash

		# Since the total_num_flags and dates_called are mutable, we don't want
		# to use them for the hash. The other pieces of data are not changed.

		# We also don't use the UO ID in the hash, per project specifications stating that
		# the UO ID should not be used as a dictionary key.s
		return (self.first_name, self.last_name, self.email_address, self.phonetic_spelling, self.reveal_code)

	def __hash__(self):
		"""
		Create a unique hash of the student. See documentation in __members()
		Having a hash is necessary for storing the students in a set, as we want
		to do in the StudentRoster class.
		"""
		return hash(self.__members())

	def __eq__(self, other):
		"""
		Tests if a Student object is equal to another object: that is, if they
		are both Students and their names, email address, phonetic spelling,
		reveal code, and UO ID are all the same.

		other: (Student) the student object to compare with self
		"""
		return isinstance(other, Student) and self.__members() == other.__members() and self.UO_ID == other.UO_ID


