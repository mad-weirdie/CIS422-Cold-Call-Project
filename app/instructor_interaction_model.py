#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Instructor Interaction Model

Description:    The main controller for the CoolCall Program.
                This module is the main driver responding to actions from the
                user. This includes receiving keyboard input, and calling the
                StudentQueue to remove/re-add students from the Queue based
                on this input. This module is also responsible for importing
                and exporting student data roster files.

Authors:        Arden Butterfield, Quinn Fetrow, Derek Martin, Amy Reichhold, 
                Madison Werries
                
Last Edited:    1/30/2022
Last Edit By:   Madison Werries
"""
###############################################################################
from tkinter import filedialog, messagebox
from display import Display
from student_queue import StudentQueue
from student_roster import StudentRoster
from log_manager import LogManager
from constants import *
###############################################################################

class InstructorInteractionModel:
    """
    A class to manage the fundamental logic of the system, and run 
    various parts of the application by calling their respective functions.

    Attributes
    =======================================================================
    index
        the index of the currently selected student in the on deck display. For
        instance, if the student furthest to the left was selected, this would
        be the integer 0.

    Methods
    =======================================================================
    ensure_directories_exist()
        Verify that specified directories exist.

    initial_loads()
        Called upon start-up: this function loads data into the queue and roster
        objects.

    _initial_load_roster()
        If the roster is not found in the internal storage location, or if the stored
        roster is not parseable, the system continues to prompt the user to import a 
        roster until one is successfully imported.

    _initial_load_queue(make_new)
        Load a queue into memory, either by loading it from the internal pickle
        file, or by creating a new queue from the roster. 

    shift_index(event)
        Called by key presses: this function shifts the index of the currently
        selected on-deck student in order to select a new student.

    remove(event)
        Called by key presses: this function removes the selected student from
        on-deck, fascilitating a cold call.

    import_roster(initial_import)
        Called if the user presses the import roster button, or upon start-up of 
        the program if there is no roster found by the system. Prompts the user to
        import a roster, notifies the user if the selected roster is not formatted
        correctly, and imports the roster into the system. 

    export_roster()
        Prompts user to select a directory, and exports the currently-loaded 
        roster file to that directory.

    _format_names(students)
        Helper function for import_roster(): formats the names of a list of
        Student objects.

"""
    def __init__(self):
        # Initialize the objects controlled by the controller class.
        self.display = Display(self)
        self.ensure_directories_exist()
        self.roster = StudentRoster()
        self.queue = StudentQueue()
        self.log_manager = LogManager("summary.txt")

        # At the start, the first student on deck will be selected.
        self.index = 0

        # We need to load the roster and queue into memory
        self.initial_loads()

        # Upon start-up, we need to tell the screen what to display.
        self.display.draw_main_screen(self.index, self.queue.get_on_deck())

        # This starts the main loop in the GUI. This continuously keeps the
        # display window visible and waits for input from the keyboard/button presses,
        # which trigger the event function that each key is mapped to.
        self.display.main_window.mainloop()

    def ensure_directories_exist(self):
        """
        Verify that specified directories exist.
        """
        try:
            os.makedirs(os.path.join(
                os.path.dirname(__file__), 'student_data'))
        except FileExistsError:
            pass
        try:
            os.makedirs(os.path.join(
                os.path.dirname(__file__), '../logs'))
        except FileExistsError:
            pass

    def initial_loads(self):
        """
        Upon start-up, the controller needs to load a roster and queue into
        memory. If there is a roster stored internally, we use that one,
        otherwise the system prompts the user to import a roster.

        Likewise, if there is already a queue stored internally, we load that
        one to memory; Otherwise, we make a new queue from the roster.

        It's important that the roster is loaded before the queue because the only
        way to make a new StudentQueue object is from a StudentRoster.
        """
        new_roster = self._inital_load_roster()
        self._initial_load_queue(new_roster)

    def _inital_load_roster(self):
        """
        Load a student roster into memory. If the roster is not found in the
        internal storage location, or if the stored roster is not parseable, the
        system continues to prompt the user to import a roster until one is successfully
        imported.

        returns: (boolean) did we make a new roster, instead of loading one from internal
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
        file, or by creating a new queue from the roster. 
        
        - If we just imported a new roster, we certainly want to make a new queue 
          or else the queue might not match the new roster. 
        - If we did not just import a new roster, then we only want to make a new
          queue if we cannot load the queue successfully from file.

        make_new: (boolean) Should we make a new queue by default?
        """
        if make_new or not self.queue.load_queue_from_file(INTERNAL_QUEUE_LOCATION):
            self.queue.queue_from_roster(self.roster)

    def shift_index(self, event):
        """
        Shift the selection index to the left or right, depending on which key
        is pressed. This method is automatically called every time the left or
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
        them, depending on which key is pressed. This method is automatically
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
        This function is called by the user pressing the "Import roster" button
        on display window.

        initial_import: (boolean) Is there no roster yet on file (initial_import=True)?
        In that case, the messages shown to the user are slightly different;
        instead of notifying about which students are changed, we notify the user
        of the full list of students in the roster.

        Returns: (boolean) True if we successfully import a roster, False otherwise.
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
                message = f"Importing this roster changes the stored data of {names}. Proceed with import?"
        
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
        Prompt the user to choose a directory, then export the currently-loaded
        roster file to that location.
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
        
        students: (list) a list of Student objects.
        """
        # Converting to set removes duplicates
        names = list(set([student.get_name() for student in
                     students]))
        # Sort alphabetical by last name, join with commas
        names= sorted(names, key=lambda name: name.split()[1] + name.split()[0])
        return ', '.join(names)
