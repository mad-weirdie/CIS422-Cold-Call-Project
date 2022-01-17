#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog, messagebox
import key_sequence
from gui import *
from student_queue import *

NUM_ON_DECK = 4

def main():
    controller = Controller()
    return 0
    
class Controller:
    def __init__(self):
        self.index = 0
        self.key_sequence = key_sequence.KeySequence()
        self.roster = StudentRoster()
        self.queue = StudentQueue()
        
        roster_found = False

        if (os.path.exists('../student_data/student_queue')):
            self.queue.load_queue_from_file('../student_data/student_queue')
        else:
            while not roster_found:
                messagebox.showinfo(
                    message="No roster found! Load a roster file from your computer.")
                self.import_roster(initial_import=True)
                roster_found = True
            self.queue.queue_from_roster(self.roster)
        
        self.display = Display(self)

        self.display.main_window.deiconify()
        self.queue.save_queue_to_file('../student_data/student_queue')
        self.on_deck = self.queue.get_on_deck()
        self.display.draw_main_screen(self.index, self.on_deck)
        self.display.main_window.mainloop()

    def shift_index_left(self, event):
        print(f"left key pressed")
        print(event)
        self.index = max((self.index - 1), 0)
        #self.add_and_check_for_random_verification(key_sequence.LEFT)
        self.display.draw_main_screen(self.index, self.on_deck)

    def shift_index_right(self, event):
        print(f"right key pressed")
        print(event)
        self.index = min((self.index + 1), 3)
        #self.add_and_check_for_random_verification(key_sequence.RIGHT)
        self.display.draw_main_screen(self.index, self.on_deck)

    def remove_without_flag(self, event):
        print("Down key pressed")
        #self.add_and_check_for_random_verification(key_sequence.DOWN)
    
        student = self.on_deck[self.index]
        student.call_on(False)
        self.queue.take_off_deck(student)
        self.queue.print_on_deck()
        self.on_deck = self.queue.get_on_deck()
        self.display.draw_main_screen(self.index, self.on_deck)

    def remove_with_flag(self, event):
        print("Up key pressed")
        #self.add_and_check_for_random_verification(key_sequence.UP)
    
        student = self.on_deck[self.index]
        student.call_on(True)
        self.queue.take_off_deck(student)
        self.queue.print_on_deck()
        self.on_deck = self.queue.get_on_deck()
        self.display.draw_main_screen(self.index, self.on_deck)

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
            names = [f"{student.first_name} {student.last_name}" for student in
                     students_who_will_be_changed]
            proceed = True
            # TODO: format the message all pretty
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
            else:
                print("Don't change roster")
        else:
            messagebox.showwarning(
                message=f"Cannot import roster file. {error}")

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

def format_names(self, list):
    """Formats a list of names into alphabetical order by last name.
    Separates them with commas and spaces."""


if __name__ == '__main__':
    main()
