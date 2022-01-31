#!/usr/bin/env python3

################################################################################
"""
Script Name:    Student Queue Class

Description:    The Student Queue Class for the CoolCall Program.
                This module is responsible for maintaining a queue of students,
                to ensure equitable cold-calling.
				
				The front of the queue represents the students who are on-deck.
				When a student is called on, the student is removed from that 
				location in the queue. They are then inserted into the back
				part of the queue, allowing the students in between to shift down.

Authors:        Arden Butterfield, Quinn Fetrow, Derek Martin, Amy Reichhold, 
				Madison Werries
                
Last Edited:    1/30/2022
Last Edit By:   Quinn Fetrow
"""
################################################################################
import random
import pickle
from student import Student
from student_roster import StudentRoster
import os
from constants import *
################################################################################

class StudentQueue:
	"""
	A class to represent a queue of students taking a course.
	
	There are two ways we can load a queue at startup: 
	- It can be created fresh from a StudentRoster.
	- Or, it can be loaded from a stored pickle file (which is preferable, since the 
	  order of students in the queue will be saved in the pickle file) 
	
	Attributes
	============================================================================
	student_queue[]
		A list of Student objects, for storing the students in the order that 
		they will be added to the on-deck display.

	Methods
	============================================================================
	queue_from_roster(roster)
		Fills out the queue from a StudentRoster object.
	load_queue_from_file(filename)
		Load a saved queue from a pickle file.
	save_queue_to_file(filename)
		Save a queue to a pickle file.
	get_on_deck()
		Get a list of the Students who are currently on-deck
	shuffle_queue()
		Randomly shuffle the entire queue.
	shuffle_front_and_back()
		Shuffle the front and back of the queue separately. This occurs at the
		start of a lecture.
	take_off_deck(student)
		Remove a Student from on deck, and re-insert the student into the queue.
	randomized_enqueue(student)
		Insert a Student into a random position in the back portion of the queue.
	dequeue_student(student)
		Remove a specific Student from the queue.
	queue_size()
		Return the number of students in the queue.
	print_queue(), print_on_deck()
		Debugging methods for printing a list of students that are stored in the queue 
		and on deck.

	"""

	# Basic constructor for the student queue.
	def __init__(self):
		"""
		Before importing from a roster or pickle file, the student queue is empty.
		"""
		self.student_queue = []

	def queue_from_roster(self, roster):
		"""
		Fill out the queue using a roster. This method is called on initial
		import when there is not a saved queue.

		roster: a StudentRoster object
		"""
		self.student_queue = []
		for student in roster.students:
			if student.include_on_deck():
				# Some of the students are marked to not be stored on deck; we
				# do not include them in the queue.
				self.student_queue.append(student)
		# Randomize the queue order to make the system more fair.
		self.shuffle_queue()
		# After every change to the queue, including creating the queue from a
		# roster, we want to save it to the file. That way the program can be shut
		# down at any moment without loss of data.
		self.save_queue_to_file(INTERNAL_QUEUE_LOCATION)

	def load_queue_from_file(self, filename):
		"""
		Fills the queue using saved queue data from a file.

		filename: (string) the name of the pickle file.
		returns: (boolean) was the file read successfully?
		"""
		try:
			infile = open(filename, 'rb')
			self.student_queue = pickle.load(infile, encoding='latin1')
			infile.close()
			self.shuffle_front_and_back()
			return True
		except Exception as e:
			return False

	def save_queue_to_file(self, filename):
		"""
		Save the queue to a pickle file.

		filename: (string) the file to save the queue to.
		"""
		outfile = open(filename, 'wb')
		pickle.dump(self.student_queue, outfile)
		outfile.close()

	def get_on_deck(self):
		"""
		Get the students who are currently on deck.

		returns:  a list of the students who are on deck.
		
		This list may be as long as <NUM_ON_DECK>, or it may be shorter
		if there are not enough students in the class whose reveal code permits
		them to be on-deck.
		"""
		on_deck = []
		for i in range(min(NUM_ON_DECK, len(self.student_queue))):
			on_deck.append(self.student_queue[i])
		return on_deck

	def shuffle_queue(self):
		"""
		Randomize the order of the entire queue.
		"""
		random.shuffle(self.student_queue)

	def shuffle_front_and_back(self):
		"""
		This function is called on startup if there is a queue saved. 
		It shuffles the front and back of the queue separately.

		We want to add some randomization to the queue, but we also want 
		to ensure that students who were just on-deck are not placed back 
		on-deck right away.
		"""
		midpoint = int(self.queue_size() * INSERT_DELAY)
		front = self.student_queue[:midpoint]
		back = self.student_queue[midpoint:]
		random.shuffle(front)
		random.shuffle(back)
		self.student_queue = front + back


	def take_off_deck(self, student):
		"""
		Remove a student from on-deck and re-insert them into the student
		queue.

		student: (Student) the student to be taken off deck
		"""
		# Wouldn't want to remove somebody from on-deck who isn't on deck...
		on_deck = self.get_on_deck()
		assert student in on_deck
		self.dequeue_student(student)
		self.randomized_enqueue(student)
		# After every change to the queue, we want to save it to the file so
		# the program can be shut down at any moment without loss of data.
		self.save_queue_to_file(INTERNAL_QUEUE_LOCATION)
	

	def randomized_enqueue(self, student):
		"""
		Insert student into a random position in the back portion of the queue.
		The part of the queue we insert into is dependent on the INSERT_DELAY
		parameter, defined in the constants file. 

		This constant defines a proportion of the front of the queue in which
		we don't want to enqueue a student.

		student: (Student) the student to be added to the queue
		"""
		# Set the insert delay such that a student can never be re-inserted into
		# an on-deck position if the queue_size > NUM_ON_DECK.
		insert_delay = INSERT_DELAY
		if (INSERT_DELAY < (NUM_ON_DECK / self.queue_size())):
			insert_delay = (NUM_ON_DECK / self.queue_size())
		start = int(self.queue_size() * insert_delay)
		stop = self.queue_size()
		rand_index = random.randint(start, stop)
		self.student_queue.insert(rand_index, student)

	def dequeue_student(self, student):
		"""
		Remove a specific student from the queue.

		student: (Student) the student to be dequeued.
		"""
		self.student_queue.remove(student)

	def queue_size(self):
		"""
		Returns the number of students currently in the queue. This is
		equivalent to the number of students in the class who are available to
		be on-deck.
		"""
		return len(self.student_queue)
	
	def print_queue(self):
		"""
		Debugging function: prints out the students in the queue.
		"""
		for i in range(len(self.student_queue)):
			print(i, " ", self.student_queue[i].get_name())
			
	def print_on_deck(self):
		"""
		Debugging function: prints out the students on deck.
		"""
		on_deck = self.get_on_deck()
		for i in range(len(on_deck)):
			print(i, " ", on_deck[i].get_name())
