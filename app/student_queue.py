################################################################################
"""
Script Name:    Student Queue Class

Description:    The Student Queue Class for the CoolCall Program.
                This module is responsible for maintaining a queue of students,
                to ensure equitable cold-calling. The front of the queue
                represents the students who are on-deck, when a student is called
                on, the student is removed from that location in the queue, and
            	added to somewhere in the back part of the queue, allowing the
            	students in between to shift down.

Authors:        EnterPrize Labs:
                Arden Butterfield, Madison Werries, Amy Reichold,
                Quinn Fetrow, and Derek Martin

Last Edited:    1/25/2022
Last Edit By:   Arden Butterfield
"""
################################################################################
import random
import pickle
from student import *
from student_roster import *
import os
from constants import *
################################################################################

class StudentQueue:
	"""
	A class to represent a single student in a course.
	Attributes
	============================================================================
	student_queue[]
		A list of Student objects, for storing the students in the order they
		will be added to the on-deck display.

	Methods
	============================================================================
	There are two ways we can load a queue at startup: either it can be loaded
	from a stored pickle file (which is preferable, since the order of students
	in the queue will be saved in the pickle file), or it can be created afresh
	from a StudentRoster.

	queue_from_roster(roster)
		Fills out the queue from a StudentRoster object.
	load_queue_from_file(filename)
		Load a saved queue from a pickle file.
	save_queue_to_file(filename)
		Save a queue to a pickle file.
	get_on_deck():
		Get a list of the Students who are on deck currently
	TODO: the rest of em
	"""
	""" Basic constructor for the student queue. """
	def __init__(self):
		self.student_queue = []

	def queue_from_roster(self, roster):
		print(roster.students)
		for student in roster.students:
			if student.include_on_deck():
				self.student_queue.insert(0, student)
		# Randomize the queue order
		self.shuffle_queue()
		print(self.student_queue)

	""" Fills the queue using saved queue data from a file. """

	def load_queue_from_file(self, filename):
		# filename = '../student_data/student_queue'
		infile = open(filename, 'rb')
		self.student_queue = pickle.load(infile, encoding='latin1')

	def save_queue_to_file(self, filename):
		#filename = '../student_data/student_queue'
		outfile = open(filename, 'wb')
		pickle.dump(self.student_queue, outfile)
		outfile.close()


		
	def get_on_deck(self):
		# TODO: only 1-3 students in the roster means they're on deck forever
		on_deck = []
		for i in range(min(NUM_ON_DECK, len(self.student_queue))):
			on_deck.append(self.student_queue[i])
		return on_deck

	""" Randomly shuffles all the students in the queue. """
	def shuffle_queue(self):
		random.shuffle(self.student_queue)

	def shuffle_front_and_back(self):
		"""
		At startup, we want to shuffle the front and the back of the queue
		separately.
		"""
		midpoint = int(self.queue_size() * INSERT_DELAY)
		front = self.student_queue[:midpoint]
		back = self.student_queue[midpoint:]
		random.shuffle(front)
		random.shuffle(back)
		self.student_queue = front + back

	""" Removes a student from on-deck and places them back into the student queue. """
	def take_off_deck(self, student):
		# Wouldn't want to remove somebody from on-deck who isn't on deck...
		on_deck = self.get_on_deck()
		assert student in on_deck
		self.dequeue_student(student)
		self.randomized_enqueue(student)
	
	"""
	Insert student into random position in the queue, but only up to a
	certain position relative to the queue size and the insert_delay factor.
	"""
	def randomized_enqueue(self, student):
		start = int(self.queue_size() * INSERT_DELAY)
		stop = self.queue_size()-1
		rand_index = random.randint(start, stop)
		self.student_queue.insert(rand_index, student)

	""" Remove a specific student from the queue. """
	def dequeue_student(self, student):
		self.student_queue.remove(student)

	""" Returns the current size of the student queue. """
	def queue_size(self):
		return len(self.student_queue)
	
	def print_queue(self):
		for i in range(len(self.student_queue)):
			print(i, " ", self.student_queue[i].get_name())
			
	def print_on_deck(self):
		on_deck = self.get_on_deck()
		for i in range(len(on_deck)):
			print(i, " ", on_deck[i].get_name())
