#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Instructor-View Controller

Description:    The main controller for the CoolCall Program.
                This module is the main driver responding to actions from the
                user. This includes receiving keyboard input, calling the
                StudentQueue to remove and re-add students from the Queue based
                on this input. The module is also responsible for the importing
                and exporting of student data roster files.

Authors:        EnterPrize Labs:
                Arden Butterfield, Madison Werries, Amy Reichold,
                Quinn Fetrow, and Derek Martin

Last Edited:    1/23/2022
Last Edit By:   Madison Werries
"""
###############################################################################
from tkinter import *
from tkinter import filedialog, messagebox
import key_sequence
from gui import *
from student_queue import *
from log_manager import *
from constants import *
###############################################################################

def main():
    controller = Controller()
    return 0
    
class Controller:
    """
    A class to manage overall logic of the system, and run the various parts of
    the application.

    Attributes
    =======================================================================
    index
        the index of the currently selected student in the on-deck display. For
        instance, if the student furthest to the left was selected, this would
        be the integer 0.

    Methods
    =======================================================================
    initial_load_queue_roster()
        Called on start-up, this function loads data into the queue and roster
        objects.
    shift_index_left(), shift_index_right()
        Called by key presses, these functions shift the index of which
        on-deck student is currently selected.
    remove_without_flag(), remove_with_flag()
        Called by key presses, these functions remove students from on-deck.
    import_roster()
        Prompts the user to import a roster, notifies them if the roster is not
        formatted correctly, and imports the roster. Called if the user presses
        the import roster button, or on start-up of the program if there is no
        roster found internally.
    export_roster()
        Prompts user for a directory, and exports the roster to that directory.
    _format_names()
        Helper function for import roster, formats the names of a list of
        Student objects.

"""
    def __init__(self):
        # Initialize the objects controlled by the controller class.
        self.display = Display(self)
        self.key_sequence = key_sequence.KeySequence()
        self.roster = StudentRoster()
        self.queue = StudentQueue()
        self.log_manager = LogManager("summary.txt")

        # At the start, the first student on deck will be selected.
        self.index = 0

        # We need to load the roster and queue into memory
        self.inital_load_queue_roster()
        self.on_deck = self.queue.get_on_deck()
        self.display.draw_main_screen(self.index, self.on_deck)
        self.display.main_window.mainloop()

    def inital_load_queue_roster(self):

        if (os.path.exists(INTERNAL_ROSTER_LOCATION)):
            self.roster.import_roster_from_file(INTERNAL_ROSTER_LOCATION)
        else:
            roster_found = False
            while not roster_found:
                messagebox.showinfo(
                    message="No roster found! Load a roster file from your computer.")
                roster_found = self.import_roster(initial_import=True)
        if (os.path.exists(INTERNAL_QUEUE_LOCATION)):
            self.queue.load_queue_from_file(INTERNAL_QUEUE_LOCATION)
        else:
            self.queue.queue_from_roster(self.roster)

    def shift_index_left(self, event):
        self.index = max((self.index - 1), 0)
        #self.add_and_check_for_random_verification(key_sequence.LEFT)
        self.display.draw_main_screen(self.index, self.on_deck)

    def shift_index_right(self, event):
        self.index = min((self.index + 1), len(self.on_deck) - 1)
        #self.add_and_check_for_random_verification(key_sequence.RIGHT)
        self.display.draw_main_screen(self.index, self.on_deck)

    def remove_without_flag(self, event):
        #self.add_and_check_for_random_verification(key_sequence.DOWN)
        student = self.on_deck[self.index]
        student.call_on(False)
        self.queue.take_off_deck(student)
        self.on_deck = self.queue.get_on_deck()
        self.display.draw_main_screen(self.index, self.on_deck)
        self.log_manager.write(self.queue.student_queue, student, False)

    def remove_with_flag(self, event):
        #self.add_and_check_for_random_verification(key_sequence.UP)
        student = self.on_deck[self.index]
        student.call_on(True)
        self.queue.take_off_deck(student)
        self.on_deck = self.queue.get_on_deck()
        self.display.draw_main_screen(self.index, self.on_deck)
        self.log_manager.write(self.queue.student_queue, student, True)

    def import_roster(self, initial_import=False):
        print("Import roster")
        filename = filedialog.askopenfilename(
            title='Choose a roster to import',
            initialdir='~')
        if not filename:
            # User hit the cancel button on the file dialog
            return
        new_roster = StudentRoster()
        error = new_roster.import_roster_from_file(filename)
    
        if not error:
            students_who_will_be_changed = new_roster.compare(self.roster)
            names = self._format_names(students_who_will_be_changed)
            proceed = True
            if initial_import:
                message = f"This roster contains the following students: {names}. Proceed with import?"
            elif len(students_who_will_be_changed) == 0:
                message = "No student data will be changed by this import. Proceed with import?"
            else:
                message = f"Importing this roster change the stored data of {names}. Proceed with import?"
        
            proceed = messagebox.askokcancel(message=message)
        
            if proceed:
                self.roster = new_roster
                print("Change roster")
                self.roster.save_internally()
                self.queue = StudentQueue()
                self.queue.queue_from_roster(self.roster)
                self.on_deck = self.queue.get_on_deck()
                self.display.draw_main_screen(self.index, self.on_deck)
                return True
            else:
                print("Don't change roster")
                return False
        else:
            messagebox.showwarning(
                message=f"Cannot import roster file. {error}")
            return False

    def export_roster(self):
        print("Export roster")
        dir_name = filedialog.askdirectory(
            title='Choose a location to save the roster',
            initialdir='~'
        )
        if not dir_name:
            # User hit the cancel button on the file dialog
            return
        path = self.roster.export_roster_to_file(dir_name)
        messagebox.showinfo(message=f"Roster exported to {path}")

    def _format_names(self, students):
        """Formats a list of names into alphabetical order by last name.
        Separates them with commas and spaces."""
        # Converting to set removes duplicates
        names = list(set([student.get_name() for student in
                     students]))
        # Sort alphabetical by last name, join with commas
        names= sorted(names, key=lambda name: name.split()[1] + name.split()[0])
        return ', '.join(names)

if __name__ == '__main__':
    main()
