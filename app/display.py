#!/usr/bin/env python3

###############################################################################
"""
Script Name:    CoolCall GUI Window Display

Description:    The visual component of the CoolCall application.

Authors:        Arden Butterfield, Quinn Fetrow, Derek Martin, Amy Reichhold,
                Madison Werries

Last Edited:    1/30/2022
Last Edit By:   Quinn Fetrow
"""
###############################################################################
from tkinter import *
from instructor_interaction_model import *
from constants import *
from random_distribution_verification import *
###############################################################################

class Display:
    """
    The Display class creates the display window and buttons.
    It formats the text and buttons of the display window to be spaced according 
    to the number of students on-deck. 

    Attributes
    =======================================================================
    rdv
        RandomVerification() is in the Display because we are mapping key presses
        to add_and_check_for_random_verification(), which is a RandomVerification() method.

    main_window
        This tkinter display window opens upon application start up when called
        by draw_main_screen(). The main_window also binds arrow key input to event
        functions from the Instructor Interaction Model.
        
    import_button
        This button is displayed on the window with the text: "Import roster".
        Clicking the button calls the import_roster function from the Instructor 
        Interaction Model, which prompts the user to specify the location of a class 
        roster file to import.

    export_button
        This button is displayed on the window with the text: "Export roster".
        Clicking the button calls the export_roster function from the Instructor 
        Interaction Model, which prompts the user to choose a directory, then exports
        the currently-loaded roster file to that location.

    labels
        Sets display window text and buttons to a specified color and format. 

    Methods
    =======================================================================
    draw_main_screen()
        This function displays the main_window to the screen along with labels and
        import/export buttons.

    """
    def __init__(self, controller):
        # The controller is the instructor_interaction_model object that
        # controls the display.
        self.rdv = RandomVerification()
        # Configure display window
        self.main_window = Tk()
        self.main_window.configure(bg="white")
        self.main_window.title("CoolCall")
        # We want the window to be as wide as the screen, but only 60 pixels
        # tall.
        self.main_window.geometry(f'{self.main_window.winfo_screenwidth()}x60')
        self.main_window.resizable(False, False)
        # Bind key presses to respective functions
        self.main_window.bind_all("<KeyRelease>", self.rdv.add_and_check_for_random_verification, True)
        self.main_window.bind_all(f"<{MOVE_LEFT_KEY}>", controller.shift_index)
        self.main_window.bind_all(f"<{MOVE_RIGHT_KEY}>", controller.shift_index)
        self.main_window.bind_all(f"<{REMOVE_WITH_FLAG_KEY}>", controller.remove)
        self.main_window.bind_all(f"<{REMOVE_WITHOUT_FLAG_KEY}>", controller.remove)
        # Create buttons
        self.import_button = Button(
            self.main_window,
            text='Import roster',
            command=controller.import_roster
        )
        self.export_button = Button(
            self.main_window,
            text='Export roster',
            command=controller.export_roster
        )
        # Configure labels
        self.labels = [
            Label(self.main_window, bg="white", fg="black", text="", width=0) for _
            in range(NUM_ON_DECK)]


    def draw_main_screen(self, selection_index, on_deck):
        """
        This function displays the main_window to the screen along with labels and
        import/export buttons.

        selection_index: (int) specifies the index of a currently selected student in the on-deck list.
        on_deck: (list) list of students who are currently on-deck.
        """
        # Create a list of on-deck names for labels
        names = []
        for i in range(len(on_deck)):
            names.append(on_deck[i].get_name())
        for i in range(len(on_deck), NUM_ON_DECK):
            names.append("")

        # Space the text and buttons in the display window according to the number of students on-deck
        self.main_window.columnconfigure(0, minsize=self.main_window.winfo_screenwidth()/(NUM_ON_DECK + 4))
        for i in range(NUM_ON_DECK):
            self.main_window.columnconfigure(i+1, minsize=self.main_window.winfo_screenwidth()/(NUM_ON_DECK + 3))
        
        # Add the "Next students: " label
        label = Label(self.main_window, bg="white", fg="black",text="Next students:", width=0)
        label.grid(row=0, column=0, padx=10, pady=20, sticky="W")

        # Make sure the display window always sits on top of other windows
        self.main_window.attributes('-topmost', True)

        # Set the color of a selected student name and unselected student names
        for i in range(NUM_ON_DECK):
            if i == selection_index:
                bg_color = "black"
                fg_color = "white"
            else:
                bg_color = "white"
                fg_color = "black"
            self.labels[i].configure(bg=bg_color)
            self.labels[i].configure(fg=fg_color)
            self.labels[i].configure(text=names[i])
            self.labels[i].grid(row=0, column=(i+1), sticky="W", rowspan=1)

        # Format the import andd export button locations
        self.import_button.grid(row=0, column=(NUM_ON_DECK + 1), columnspan=1, padx=20)
        self.export_button.grid(row=0, column=(NUM_ON_DECK + 2), columnspan=1, padx=3)