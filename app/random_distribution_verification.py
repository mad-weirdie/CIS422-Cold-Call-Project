#!/usr/bin/env python3

from tkinter import filedialog, messagebox
from turtle import left
from key_sequence import *
from student_roster import *
from student_queue import *
from random import randrange
from constants import *
from datetime import *
from os.path import exists
from student import Student

##################################################################################################################

class RandomVerification:
    #   Restart the program 100 times
    #   Issue 100 random cold calls each time the program restarts (10,000 total)
    #   All 10,000 cold calls should go to the same "Rand Dist" output file.
    #   Overwrite this file each time the instructor enters Random Distribution Verification Mode

    ##############################################################################################################

    def __init__(self):
        self.key_sequence = KeySequence()

    ##############################################################################################################

    def add_and_check_for_random_verification(self, event):
        # Will get called by the GUI every time a key is pressed."""
        self.key_sequence.add_key(event.keysym)
        if self.key_sequence.check_for_match():
            self.start()
            self.key_sequence.reset()

    ##############################################################################################################

    def start(self):
        do_random_verification = messagebox.askokcancel(
            message="You have entered Randomness Distribution Verification Mode. A dedicated output file for this Mode will be created. If it already exists, it will be overwritten. Do you want to proceed?"
        )
        if do_random_verification:

            self.output_file = open(f"{LOGS_LOCATION}/random_distribution_verification.txt", "w+")
            self.write_header()
            self.create_test_queue()
            self.run()
            self.output_file.close()
    
    ##############################################################################################################

    def create_test_queue(self):
        #   NOTE:   After running Rand Dist Verficiation, we probably want the queue to be how it was before.
        #           So, we should either make a copy of the queue from Roster class, or import a new test queue from Pickle file.

        self.test_queue = StudentQueue()

        roster_found = False
        if (os.path.exists(INTERNAL_QUEUE_LOCATION)):
            self.test_queue.load_queue_from_file(INTERNAL_QUEUE_LOCATION)
        else:
            while not roster_found:
                roster_found = True
                self.test_queue.queue_from_roster(INTERNAL_ROSTER_LOCATION)

    ##############################################################################################################

    def random_call(self):
        # TODO: call a random student from on deck
        on_deck = self.test_queue.get_on_deck()
        student_index = randrange(NUM_ON_DECK)
        student = on_deck[student_index]
        self.test_queue.take_off_deck(student)
        on_deck = self.test_queue.get_on_deck()
        self.write_line(student)

    ##############################################################################################################

    def run(self):
        for i in range(100):
            # call randomization function from student_queue to simulate an application restart
            self.test_queue.shuffle_front_and_back()
            for i in range(100):
                self.random_call()

    ##############################################################################################################

    def write_header(self):
        self.output_file.write("Random Distribution Verification Mode\n")
        date_line = f"Tested on {datetime.today().strftime('%Y-%m-%d')}\n\n"
        self.output_file.write(date_line)

    ##############################################################################################################

    def write_line(self, student):
        # write line
        cold_call = f"{student.first_name} {student.last_name}\n"
        self.output_file.write(cold_call)