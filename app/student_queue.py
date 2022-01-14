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
insert_delay = 0.35

class StudentQueue:
	student_queue = []

	""" Basic constructor for the student queue. """
	def __init__(self):
		student_queue = []

	""" Fills the queue using data from an instance of the roster class. """
	def queue_from_roster(self, roster):
		for student in roster.student_list:
			self.student_queue.insert(0, student)
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
		on_deck = []
		for i in range(num_on_deck):
			print("i: ", i, "student: ", self.student_queue[i].get_name())
			on_deck.append(self.student_queue[i])
		assert(len(on_deck) == num_on_deck)
		return on_deck

	""" Randomly shuffles all the students in the queue. """
	def shuffle_queue(self):
		random.shuffle(self.student_queue)

	""" Removes a student from on-deck and places them back into the student queue. """
	def take_off_deck(self, student):
		# Wouldn't want to remove somebody from on-deck who isn't on deck...
		on_deck = self.get_on_deck()
		assert student in on_deck
		
		print("Student's index prior to dequeue: ", self.student_queue.index(student))
		self.dequeue_student(student)
		print(len(self.student_queue))
		self.randomized_enqueue(student)
		print("Student's index post enqueue: ", self.student_queue.index(student))
		print(len(self.student_queue))
	
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
		print(len(self.student_queue))
		self.student_queue.remove(student)
		print(len(self.student_queue))

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
