#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Random Distrubtion Verification Mode

Description:    The system admin or instructor may enter this mode to verify that
                the queue randomization functionality is working properly. This is
                to ensure that students are cold called at an even rate compared to
                other students.

Authors:        Arden Butterfield, Quinn Fetrow, Derek Martin, Amy Reichhold, 
                Madison Werries

Last Edited:    1/30/2022
Last Edit By:   Madison Werries
"""
###############################################################################
from tkinter import filedialog, messagebox
from key_sequence import KeySequence
from student_queue import StudentQueue
from student_roster import StudentRoster
from random import randrange
from constants import *
from datetime import *
##################################################################################################################

class RandomVerification:
    """
    A class for operating Random Distribution Verification Mode.
    This mode is meant to restart the program 100 times, and issue
    100 random cold calls each time the program restarts (10,000 total 
    cold calls).

    In order to simulate a pseudo-restart of the program, we call the
    shuffle_front_and_back() method on the test queue. This effect is
    consistent with actually restarting the program.

    All 10,000 cold calls are recorded in a separate log file called
    'random_distribution_verification.txt'. 
    
    Then, an additional summary file is created called 'RDV_summary.txt'.
    
    The summary file shows the amount oftimes each student was cold called 
    during the most recent RDV run, while the log file shows a list of all 
    cold calls in order. Both output files are overwritten by every RDV run.

    """

    def __init__(self):
        self.key_sequence = KeySequence()
        self.roster = StudentRoster()
        self.roster.import_roster_from_file(INTERNAL_ROSTER_LOCATION)
        self.names = []
        for student in self.roster.students:
            self.names.append(student.get_name())
        self.output_file = open(f"{LOGS_LOCATION}/random_distribution_verification.txt", "w+")
        self.summary_data = {}

    def add_and_check_for_random_verification(self, event):
        """
        Called by the Display every time a key is pressed.
        This sends the pressed key to key_sequence.py to check
        if the system should enter RDV mode.
        """
        self.key_sequence.add_key(event.keysym)
        if self.key_sequence.check_for_match():
            self.start()
            self.key_sequence.reset()

    def start(self):
        """
        Prompt the user to confirm that they want to run Random Distribution Verification Mode.
        Then, create the output files and call the run() method.
        """
        # Warn the user that the output file will be overwritten.
        do_random_verification = messagebox.askokcancel(
            message="You have entered Randomness Distribution Verification Mode. A dedicated output file for this Mode will be created. If it already exists, it will be overwritten. Do you want to proceed?"
        )
        # If the user confirms that they want to run RDV, continue
        if do_random_verification:
            self.write_header()
            self.create_test_queue()
            self.run()
            self.output_file.close()
            self.summarize_RDV()
            messagebox.showinfo(
                message="Random Distribution Verification Mode has completed successfully. Returning to normal CoolCall mode."
            )
    
    def summarize_RDV(self):
        """
        Create a summary file, recording the amount of times that each student was cold called 
        during the most recent RDV run.
        """
        f = open(f"{LOGS_LOCATION}/random_distribution_verification.txt", "r")
        lines = f.readlines()
        summary = open(f"{LOGS_LOCATION}/RDV_summary.txt", "w+")
        for student in self.names:
            self.summary_data[student] = 0
        for name in lines:
            name = name.strip()
            if name in self.names:
                    self.summary_data[name] = self.summary_data[name] + 1
        summary.write("A summary file of the data created during Random Distribution Verification Mode.\n")
        for student in self.names:
            summary.write("{0}\t{1}\n".format(student, self.summary_data[student]))
        f.close()
            
    def create_test_queue(self):
        """
        Create a test queue from the roster file so that the actual queue is not overwritten.
        If the queue file cannot be located, the test queue is created from the roster file.
        """
        self.test_queue = StudentQueue()
        roster_found = False
        if (os.path.exists(INTERNAL_QUEUE_LOCATION)):
            self.test_queue.load_queue_from_file(INTERNAL_QUEUE_LOCATION)
        else:
            self.test_queue.queue_from_roster(INTERNAL_ROSTER_LOCATION)

    def random_call(self):
        """
        Call a random student from on-deck. Record this in the log file.
        """
        on_deck = self.test_queue.get_on_deck()
        # Randomly select an on-deck student
        student_index = randrange(NUM_ON_DECK)
        student = on_deck[student_index]
        self.test_queue.take_off_deck(student)
        on_deck = self.test_queue.get_on_deck()
        self.write_line(student)

    def run(self):
        """
        Main loop.
        Randomize the queue 100 times, and each time it's been randomized, cold call 100 students.
        """
        for i in range(100):
            # call function from student_queue.py to simulate an application restart
            self.test_queue.shuffle_front_and_back()
            for i in range(100):
                self.random_call()

    def write_header(self):
        """
        Write the header to the log file.
        """
        self.output_file.write("Random Distribution Verification Mode\n")
        # Include the date.
        date_line = f"Tested on {datetime.today().strftime('%Y-%m-%d')}\n\n"
        self.output_file.write(date_line)

    def write_line(self, student):
        """
        Write one line to the log file per cold call
        """
        cold_call = f"{student.first_name} {student.last_name}\n"
        self.output_file.write(cold_call)