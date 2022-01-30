#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Cool Call GUI Window Display

Description:    The visual component of the Cold Call application. 
                This module creates the display window of the GUI, and binds arrow 
                key input to event functions from the main controller (instructor_interaction_model.py).

Authors:        EnterPrize Labs:
                Arden Butterfield, Madison Werries, Amy Reichold,
                Quinn Fetrow, and Derek Martin

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
    to the number of students on deck. 
    """

    def __init__(self, controller):
        self.rdv = RandomVerification()
        self.main_window = Tk()
        self.main_window.configure(bg="white")
        self.main_window.title("Cold Call application")
        self.main_window.geometry(f'{self.main_window.winfo_screenwidth()}x60')
        self.main_window.resizable(False, False)
        self.main_window.bind_all("<KeyRelease>", self.rdv.add_and_check_for_random_verification, True)
        self.main_window.bind_all(f"<{MOVE_LEFT_KEY}>", controller.shift_index)
        self.main_window.bind_all(f"<{MOVE_RIGHT_KEY}>", controller.shift_index)
        self.main_window.bind_all(f"<{REMOVE_WITH_FLAG_KEY}>", controller.remove)
        self.main_window.bind_all(f"<{REMOVE_WITHOUT_FLAG_KEY}>", controller.remove)
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
        self.labels = [
            Label(self.main_window, bg="white", fg="black", text="", width=0) for i
            in range(NUM_ON_DECK)]


    def draw_main_screen(self, selection_index, on_deck):
        names = []
        for i in range(len(on_deck)):
            names.append(on_deck[i].get_name())
        for i in range(len(on_deck), NUM_ON_DECK):
            names.append("")

        self.main_window.columnconfigure(0, minsize=self.main_window.winfo_screenwidth()/(NUM_ON_DECK + 4))
        for i in range(NUM_ON_DECK):
            self.main_window.columnconfigure(i+1, minsize=self.main_window.winfo_screenwidth()/(NUM_ON_DECK + 3))
        
        label = Label(self.main_window, bg="white", fg="black",text="Next students:", width=0)
        self.main_window.attributes('-topmost', True)
        label.grid(row=0, column=0, padx=10, pady=20, sticky="W")
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

        self.import_button.grid(row=0, column=(NUM_ON_DECK + 1), columnspan=1, padx=20)
        self.export_button.grid(row=0, column=(NUM_ON_DECK + 2), columnspan=1, padx=3)