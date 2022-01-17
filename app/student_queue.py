#!/usr/bin/env python3
from student import *
"""
The core structure and functionality of the Student Queue.
"""

import random
import pickle
from student_roster import *
import os

# Global variable for the number of students the instructor would like to have
# "on deck" from the queue at any given time.
num_on_deck = 4
# Don't insert students back into the queue at a certain percentage of the head.
insert_delay = 0.35

class StudentQueue:
	student_queue = []

	""" Basic constructor for the student queue. """
	def __init__(self):
		student_queue = []

	""" Fills the queue using data from an instance of the roster class. """
	def queue_from_roster(self, roster):
		for student in roster.students:
			self.student_queue.insert(0, student)
		# Randomize the queue order
		self.shuffle_queue()

	def save_queue_to_file(self, filename):
		#filename = '../student_data/student_queue'
		outfile = open(filename, 'wb')
		pickle.dump(self.student_queue, outfile)
		outfile.close()

	""" Fills the queue using saved queue data from a file. """
	def load_queue_from_file(self, filename):
		#filename = '../student_data/student_queue'
		infile = open(filename, 'rb')
		self.student_queue = pickle.load(infile, encoding='latin1')
		
	def get_on_deck(self):
		# TODO: only 1-3 students in the roster means they're on deck forever
		on_deck = []
		for i in range(num_on_deck):
			on_deck.append(self.student_queue[i])
		assert(len(on_deck) == num_on_deck)
		return on_deck

	""" Randomly shuffles all the students in the queue. """
	def shuffle_queue(self):
		random.shuffle(self.student_queue)

	def shuffle_front_and_back(self):
		"""
		At startup, we want to shuffle the front and the back of the queue
		separately.
		"""
		midpoint = int(self.queue_size() * insert_delay)
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
		start = int(self.queue_size() * insert_delay)
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
