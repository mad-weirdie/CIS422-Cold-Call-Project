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

    def add_and_check_for_random_verification(self, new_key):
        """ Will get called by the controller every time a key is pressed."""
        self.key_sequence.add_key(new_key)
        if self.key_sequence.check_for_match():
            print("Match! do random verification mode")
            self.start()
            self.key_sequence.reset()
        else:
            print("No match")

    def start(self):
        do_random_verification = messagebox.askokcancel(
            message="You have entered Randomness Distribution Verification Mode. A dedicated output file for this Mode will be created. If it already exists, it will be overwritten. Do you want to proceed?"
        )
        if do_random_verification:
            self.create_output_file()
            self.run()
    
    ##############################################################################################################

    def create_output_file(self):
        self.out = open("random_distribution_verification.txt", "w+")

    ##############################################################################################################

    def restart_app(self):
        controller = Controller()

    ##############################################################################################################

    def generate_hundred_calls(self):
        for i in range(100):
            # call the controller file here
            

            result = "" # format the cold call info into a string?
            self.write_to_output_file(result)


    ##############################################################################################################

    def write_to_output_file(self, result):
        self.out.write(result + "\n")
        pass

    ##############################################################################################################

    def run(self):
        for i in range(100):
            self.restart_app()
            self.generate_hundred_calls()

##################################################################################################################
            
RDV = RandomVerification()
RDV.start()


"""

"""