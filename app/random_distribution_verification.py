#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, messagebox
from key_sequence import *
from controller import *
from student_roster import *
from student_queue import *

##################################################################################################################

class RandomVerification:
    #   Restart the program 100 times
    #   Issue 100 random cold calls EACH TIME the program restarts (10,000 total)
    #   All 10,000 cold calls should go to the same "Rand Dist" output file.
    #   Overwrite this file each time the instructor enters Random Distribution Verification Mode

    ##############################################################################################################

    def __init__(self, controller):
        self.key_sequence = key_sequence.KeySequence()
        self.controller = controller

    ##############################################################################################################

    def add_and_check_for_random_verification(self, new_key):
        """ Will get called by the controller every time a key is pressed."""
        self.key_sequence.add_key(new_key)
        if self.key_sequence.check_for_match():
            self.start()
            self.key_sequence.reset()

    ##############################################################################################################

    def start(self):
        do_random_verification = messagebox.askokcancel(
            message="You have entered Randomness Distribution Verification Mode. A dedicated output file for this Mode will be created. If it already exists, it will be overwritten. Do you want to proceed?"
        )
        if do_random_verification:
            self.create_output_file()
            self.create_test_queue()
            self.run()
    
    ##############################################################################################################

    def create_output_file(self):
        self.out = open("random_distribution_verification.txt", "w+")

    ##############################################################################################################

    def create_test_queue(self):
        #   Should the test queue be created from an instance of Roster class, or imported from a file?
        #   NOTE:   After running Rand Dist Verficiation, we probably want the queue to be how it was before.
        #           So, either make a copy of the queue from Roster class, or import a new test queue from Pickle file.

        self.test_queue = StudentQueue()
        self.test_queue.queue_from_roster(roster)   #TODO: specify the roster file to import

    ##############################################################################################################

    def restart_app(self):
        # call randomization function from student_queue to simulate an application restart
        self.test_queue.shuffle_front_and_back()

    ##############################################################################################################

    def generate_hundred_cold_calls(self):
        for i in range(100):
            # call the controller file here
            self.test_queue.take_off_deck(student)  #TODO: Determine which student to dequeue
            result = student                        #TODO: Figure out what to write to output file
            self.write_to_output_file(result)

    ##############################################################################################################

    def write_to_output_file(self, result):
        self.out.write(result + "\n")

    ##############################################################################################################

    def run(self):
        for i in range(100):
            self.restart_app()
            self.generate_hundred_cold_calls()

##################################################################################################################
            
RDV = RandomVerification()
RDV.start()