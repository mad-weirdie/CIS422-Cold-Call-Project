#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, messagebox
import key_sequence
from student_roster import *
from student_queue import *

NUM_ON_DECK = 4

class Controller:
    def __init__(self):
        self.index = 0
        self.main_window = Tk()
        self.main_window.configure(bg="white")
        self.main_window.title("Cold Call application")
        self.main_window.geometry("600x100")

        self.import_button = Button(
            self.main_window,
            text='Import roster',
            command=self.import_roster
        )

        self.export_button = Button(
            self.main_window,
            text='Export roster',
            command=self.export_roster
        )

        self.key_sequence = key_sequence.KeySequence()

        self.main_window.bind_all("<Left>", self.shift_index_left)
        self.main_window.bind_all("<Right>", self.shift_index_right)
        self.main_window.bind_all("<Up>", self.remove_with_flag)
        self.main_window.bind_all("<Down>", self.remove_without_flag)

        self.queue = StudentQueue()
        self.roster = StudentRoster()
        self.on_deck = [None for i in range(4)]
        self.labels = [
            Label(self.main_window, bg="white", fg="black", text="", width=0) for i
            in range(4)]

    def draw_main_screen(self):
        l = Label(self.main_window, bg="white", fg="black",text="Next students:", width=0)
        l.grid(row=0, column=0, padx=10, pady=20)
        for n in range(4):
            if n == self.index:
                bg_color = "black"
                fg_color = "white"
            else:
                bg_color = "white"
                fg_color = "black"
            self.labels[n].configure(bg=bg_color)
            self.labels[n].configure(fg=fg_color)
            self.labels[n].configure(text=self.on_deck[n].get_name())
            self.labels[n].grid(row=0, column=n+1)

        self.import_button.grid(row=1, column=0, columnspan=2)
        self.export_button.grid(row=1, column=2, columnspan=2)

    def format_names(self, list):
        """Formats a list of names into alphabetical order by last name.
        Separates them with commas and spaces."""


    def import_roster(self, initial_import=False):
        print("Import roster")
        filename = filedialog.askopenfilename(
            title='Choose a roster to import',
            initialdir='~')
        if not filename:
            # User hit the cancel button on the file dialog
            return
        #TODO: call the real functions
        #TODO: check if file is readable

        self.roster.import_roster_from_file(filename)
        """
        file_is_readable = True
        if file_is_readable:
            students_who_will_be_changed = ["Abc Def", "Qwert Tyui", "Axcv Vbnm"]
            # TODO: call real function to get the names
            proceed = True
            # TODO: format the message all pretty
            if initial_import:
                message = f"This roster contains the following students: {students_who_will_be_changed}"
            elif len(students_who_will_be_changed) == 0:
                message = "No student data will be changed by this import. Proceed?"
            else:
                message = f"Importing this roster change the stored data of {students_who_will_be_changed}. Proceed?"

            proceed = messagebox.askokcancel(message=message)

            if proceed:
                # TODO: Change the roster
                print("Change roster")
            else:
                print("Don't change roster")
        else:
            # TODO: the message could be returned from the file reader program, for more descriptivity.
            messagebox.showwarning(message="The roster you selected is not formatted correctly.")
        """
        self.queue.queue_from_roster(self.roster)
        self.on_deck = self.queue.get_on_deck()

    def export_roster(self):
        print("Export roster")
        filename = filedialog.askdirectory(
            title='Choose a location to save the roster',
            initialdir='~'
        )
        if not filename:
            # User hit the cancel button on the file dialog
            return

    def random_verication(self):
        # TODO: check if data will be overwritten, that is, does an output data file exist?
        data_will_be_overwritten = False
        if data_will_be_overwritten:
            do_random_verification = messagebox.askokcancel(
                message="The keystroke sequence you pressed triggers the randomness distribution verification mode. This will overwrite data in the output data file. Proceed with this test?"
            )
        else:
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

    def shift_index_left(self, event):
        print(f"left key pressed")
        print(event)
        self.index = max((self.index - 1), 0)
        self.add_and_check_for_random_verification(key_sequence.LEFT)
        self.draw_main_screen()

    def shift_index_right(self, event):
        print(f"right key pressed")
        print(event)
        self.index = min((self.index + 1), 3)
        self.add_and_check_for_random_verification(key_sequence.RIGHT)
        self.draw_main_screen()

    def remove_without_flag(self, event):
        print("Down key pressed")
        self.add_and_check_for_random_verification(key_sequence.DOWN)

        student = self.on_deck[self.index]
        student.call_on(False)
        self.queue.take_off_deck(student)
        self.queue.print_on_deck()
        self.on_deck = self.queue.get_on_deck()
        self.draw_main_screen()

    def remove_with_flag(self, event):
        print("Up key pressed")
        self.add_and_check_for_random_verification(key_sequence.UP)

        student = self.on_deck[self.index]
        student.call_on(True)
        self.queue.take_off_deck(student)
        self.queue.print_on_deck()
        self.on_deck = self.queue.get_on_deck()
        self.draw_main_screen()


    def show(self):
        self.main_window.mainloop()

    def run(self):
        # Hide the main window until after initial import
        self.main_window.withdraw()
        roster_found = False
        while not roster_found:
            messagebox.showinfo(
                message="No roster found! Load a roster file from your computer.")
            self.import_roster(initial_import=True)
            # TODO: if the import went correctly...
            roster_found = True
        # Make main window visible again.
        self.main_window.deiconify()
        self.draw_main_screen()
        self.show()

a = Controller()
a.run()