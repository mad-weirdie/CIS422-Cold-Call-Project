#!/usr/bin/env python3
from student import *
import random
"""
The core structure and functionality of the Student Queue.
"""
# Global variable for the number of students the instructor would like to have
# "on deck" from the queue at any given time.
num_on_deck = 4
# Don't insert students back into the queue at a certain percentage of the head.
insert_delay = 0.2

class StudentQueue:
	student_queue = []

	""" Basic constructor for the student queue. """
	def __init__(self):
		student_queue = []

	""" Fills the queue using data from an instance of the roster class. """
	def queue_from_roster(self, roster):
		for student in roster.student_list:
			self.student_queue.append(student)
		# Randomize the queue order
		self.shuffle_queue()

	def save_queue_to_file(self, filename):
		# TODO: FIGURE OUT EXACTLY WHAT FORMAT TO STORE THE QUEUE IN
		f = open(filename, "w")
		for student in self.student_queue:
			f.write(student)

	""" Fills the queue using saved queue data from a file. """
	def load_queue_from_file(self, queue):
		# TODO: FIGURE OUT EXACTLY WHAT FORMAT TO STORE THE QUEUE IN - pickle! :)
		for student in queue:
			# Maintain the previous queue
			self.student_queue.append(student)

	def get_on_deck(self):
		# TODO: only 1-3 students in the roster means they're on deck forever
		start = self.queue_size() - num_on_deck
		stop = self.queue_size()
		on_deck = []
		for i in range(start, stop):
			on_deck.append(self.student_queue[i])
		assert(len(on_deck) == num_on_deck)
		return on_deck

	""" Randomly shuffles all the students in the queue. """
	def shuffle_queue(self):
		random.shuffle(self.student_queue)

	"""
	Insert student into random position in the queue, but only up to a
	certain position relative to the queue size and the insert_delay factor.
	"""
	def randomized_enqueue(self, student):
		stop = int(self.queue_size() * (1-insert_delay))
		rand_index = random.randint(0, stop)
		self.student_queue.insert(rand_index, student)

	""" Remove a specific student from the queue. """
	def dequeue_student(self, student):
		self.student_queue.remove(student)

	""" Returns the current size of the student queue. """
	def queue_size(self):
		return len(self.student_queue)