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

Last Edited:    1/26/2022
Last Edit By:   Arden Butterfield
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
    initial_loads()
        Called on start-up, this function loads data into the queue and roster
        objects.
    shift_index()
        Called by key presses, this function shifts the index of which
        on-deck student is currently selected.
    remove()
        Called by key presses, this function removes the selected student from
        on-deck.
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
        self.initial_loads()

        # At start-up, we need to tell the screen what to display.
        self.display.draw_main_screen(self.index, self.queue.get_on_deck())

        # This starts the main loop in the GUI. This continuously keeps the
        # screen visible and waits for input from the keyboard/button presses,
        # which trigger the functions those keys are mapped to.
        self.display.main_window.mainloop()


    def initial_loads(self):
        """
        At start-up, the controller needs to load a roster and queue into
        memory. If there is a roster stored internally, we use that one,
        otherwise the system prompts the user to import a roster.
        Likewise, if there is already a queue stored internally, we load that
        one to memory; Otherwise, we make a new queue from the roster.

        It's important that the roster is loaded before the queue: as the only
        way to make a new StudentQueue object is from a StudentRoster.
        """
        new_roster = self._inital_load_roster()
        self._initial_load_queue(new_roster)

    def _inital_load_roster(self):
        """
        Load a roster into memory. If the roster is not found in the internal
        storage location, or the stored roster is not parseable, the system
        prompts the user to import a roster until one is successfully
        imported.

        returns: did we make a new roster, instead of loading one from internal
        storage?
        """
        new_roster = False
        errors = self.roster.import_roster_from_file(INTERNAL_ROSTER_LOCATION)
        if errors:

            while not new_roster:
                messagebox.showinfo(
                    message="No roster found! Load a roster file from your computer.")
                new_roster = self.import_roster(initial_import=True)
        return new_roster

    def _initial_load_queue(self, make_new):
        """
        Load a queue into memory, either by loading it from the internal pickle
        file, or by creating a new queue from the roster. If we just imported a
        new roster, we certainly want to make a new queue, or else the queue
        might not match the new roster. Otherwise, we only want to make a new
        queue if we cannot load the queue from the file successfully.

        make_new: (boolean) Should we make a new queue by default?
        """
        if make_new or not self.queue.load_queue_from_file(INTERNAL_QUEUE_LOCATION):
            self.queue.queue_from_roster(self.roster)

    def shift_index(self, event):
        """
        Shift the selection index left or right, depending on which key is
        pressed. This method is automatically called every time the left or
        right keys (or other keys, as defined in constants.py) are pressed.

        event: the Tkinter event of the keypress.
        """
        if event.keysym == MOVE_LEFT_KEY:
            self.index = max((self.index - 1), 0)
        elif event.keysym == MOVE_RIGHT_KEY:
            self.index = min((self.index + 1), len(self.queue.get_on_deck()) - 1)
        else:
            raise ValueError(f"Event {event} should not have triggered the shift_index method.")
        self.display.draw_main_screen(self.index, self.queue.get_on_deck())

    def remove(self, event):
        """
        Remove the selected student from the queue, with or without flagging
        them, depending on which keys are pressed. This method is automatically
        called every time the up or down keys (or other keys, as defined in
        constants.py) are pressed.

        event: the Tkinter event of the keypress.
        """
        student = self.queue.get_on_deck()[self.index]
        if event.keysym == REMOVE_WITH_FLAG_KEY:
            flag = True
        elif event.keysym == REMOVE_WITHOUT_FLAG_KEY:
            flag = False
        else:
            raise ValueError(f"Event {event} should not have triggered the remove method.")

        student.call_on(flag)
        self.queue.take_off_deck(student)
        self.log_manager.write(self.queue.student_queue, student, flag)
        self.display.draw_main_screen(self.index, self.queue.get_on_deck())

    def import_roster(self, initial_import=False):
        """
        Prompt the user through the steps for importing a roster.
        This function is called by the user pressing the "Import Roster" button
        on screen.

        initial_import: Is there no roster yet on file (initial_import is true)?
        In that case, the messages that the system shows the user are slightly
        different; instead of notifying about which students are changed, we
        notify the user the full list of students in the roster.

        Returns: True if we successfully import a roster, False otherwise.
        """
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
                self.display.draw_main_screen(self.index, self.queue.get_on_deck())
                return True
            else:
                print("Don't change roster")
                return False
        else:
            messagebox.showwarning(
                message=f"Cannot import roster file. {error}")
            return False

    def export_roster(self):
        """
        Prompts the user to chose a directory, then exports the directory to
        that location.
        """
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
        """
        Helper function for message dialogs when importing a roster.
        Formats a list of names into alphabetical order by last name.
        Separates them with commas and spaces.
        students is a list of Student objects."""
        # Converting to set removes duplicates
        names = list(set([student.get_name() for student in
                     students]))
        # Sort alphabetical by last name, join with commas
        names= sorted(names, key=lambda name: name.split()[1] + name.split()[0])
        return ', '.join(names)

if __name__ == '__main__':
    main()
