#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, messagebox
import key_sequence
from student_roster import *
from student_queue import *

NUM_ON_DECK = 4

class RandomVerification:

    def random_verication(self):
        # NOTE: Make sure no data gets overwritten. Always make a new output file for Rand. Dist. Verfication Mode

        do_random_verification = messagebox.askokcancel(
            message="The keystroke sequence you pressed triggers the randomness distribution verification mode. Proceed with this test?"
        )
        if do_random_verification:
            # TODO Do the random verification process
            pass


    def add_and_check_for_random_verification(self, new_key):
        self.key_sequence.add_key(new_key)
        if self.key_sequence.check_for_match():
            print("Match! do random verification mode")
            self.random_verication()
            self.key_sequence.reset()

        else:
            print("No match")