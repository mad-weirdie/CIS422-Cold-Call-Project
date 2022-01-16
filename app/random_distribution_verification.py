#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, messagebox
import key_sequence
from student_roster import *
from student_queue import *

##################################################################################################################

class RandomVerification:
    #   Restart the program 100 times
    #   Issue 100 random cold calls EACH TIME the program restarts (10,000 total)
    #   All 10,000 cold calls should go to the same "Rand Dist" output file.
    #   Overwrite this file each time the instructor enters Random Distribution Verification Mode

    ##############################################################################################################

    def start(self):
        do_random_verification = messagebox.askokcancel(
            message="You have entered Randomness Distribution Verification Mode. A dedicated output file for this Mode will be created. If it already exists, it will be overwritten. Proceed?"
        )
        if do_random_verification:
            self.create_output_file()
            self.run()
    
    ##############################################################################################################

    def create_output_file(self):
        self.out = open("random_distribution_verification.txt", "w+")

    ##############################################################################################################

    def restart_app(self):
        pass

    ##############################################################################################################

    def generate_hundred_calls(self):
        for i in range(100):
            result = ""
            self.write_to_output_file(result)
        pass

    ##############################################################################################################

    def write_to_output_file(self, result):
        self.out.write(result + "\n")
        pass

    ##############################################################################################################

    def run(self):
        for i in range(100):
            self.generate_hundred_calls()
            self.restart_app()

##################################################################################################################
            
RDV = RandomVerification()
RDV.start()









"""
def add_and_check_for_random_verification(self, new_key):
    self.key_sequence.add_key(new_key)
    if self.key_sequence.check_for_match():
        print("Match! do random verification mode")
        self.random_verication()
        self.key_sequence.reset()

    else:
        print("No match")
"""