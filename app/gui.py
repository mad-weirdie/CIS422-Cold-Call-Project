#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, messagebox
import key_sequence

class Display:
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

        self.names = ["Alice Alison","Bob Bobbert", "Claire Clairvoyant", "Dave David"]

    def draw_main_screen(self):
        for n in range(4):
            if n == self.index:
                bg_color = "black"
                fg_color = "white"
            else:
                bg_color = "white"
                fg_color = "black"
            l = Label(self.main_window, bg=bg_color, fg=fg_color, text=self.names[n], width=0)
            l.grid(row=0, column=n,padx=10,pady=20)
        self.import_button.grid(row=1, column=0, columnspan=2)
        self.export_button.grid(row=1, column=2, columnspan=2)

    def import_roster(self):
        print("Import roster")
        filename = filedialog.askopenfilename(
            title='Choose a roster to import',
            initialdir='~')
        if not filename:
            # User hit the cancel button on the file dialog
            return
        #TODO: call the real functions
        file_is_readable = True
        if file_is_readable:
            students_who_will_be_changed = ["Alice", "Bob", "Eve"]
            # TODO: call real function to get the names
            proceed = True
            # TODO: format the message all pretty
            proceed = messagebox.askokcancel(
                message=f"Importing this roster change the stored data of {students_who_will_be_changed}. Proceed?")
            """for student in students_who_will_be_changed:
                proceed = messagebox.askyesno(message=f"This will change the stored data of {student}. Proceed?")
                if proceed == False:
                    break"""
            if proceed:
                # TODO: Change the roster
                print("Change roster")
            else:
                print("Don't change roster")
        else:
            # TODO: the message could be returned from the file reader program, for more descriptivity.
            messagebox.showwarning(message="The roster you selected is not formatted correctly.")

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
        # TODO: handle this

    def remove_with_flag(self, event):
        print("Up key pressed")
        self.add_and_check_for_random_verification(key_sequence.UP)
        # TODO: handle this

    def show(self):
        self.main_window.mainloop()

    def run(self):
        self.draw_main_screen()
        self.show()

a = Display()
a.run()