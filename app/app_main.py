#!/usr/bin/env python3

"""
I started messing around with gui using tkinter:

What it does so far: opens display with names, accepts keyboard input.
On keyboard input, runs function that lets you change the names/highlighted
index of the display.

What it does not do: I still need to figure out how to make it still accept
keyboard input while the display is in the background, and how to make it
sit on top of other apps.
"""

from tkinter import *
from student_roster import *
from student_queue import *

# TODO: On startup, no names highlighted until an L/R arrow key is pressed
# TODO: All numerical parameters, and all keystroke assignments, discussed in the specification must be set
#  at the top of a source code file, and easily changeable by a programmer during development and
#  maintenance of the code.

# names = ["Alice Alison", "Bob Bobbert", "Claire Clairvoyant", "Dave David"]
on_deck = []
names = []
num_on_deck = 4     # NOTE: <--- This should be controlling the variable of the same name in student_queue
index = 0
queue = StudentQueue()

""" Main function called on startup """
def main():
    global on_deck

    # TODO: PROMPT INSTRUCTOR FOR FILE INPUT!
    # Create a new roster
    roster = StudentRoster()
    roster.import_roster_from_file("../input_data/roster.txt")

    # Load roster into a queue
    queue.queue_from_roster(roster)
    
    # Get list of students who are on deck
    on_deck = queue.get_on_deck()
    for student in on_deck:
        names.append(student.get_name())
        
    return 0

def key_pressed(event):
    global on_deck, index, names
    print(f"key pressed: {event.keysym}")

    # NOTE: Key pressed left: move left
    if (event.keysym == "Left"):
        if (index - 1 >= 0):
            index = index - 1

    # NOTE: Key pressed right: move right
    if (event.keysym == "Right"):
        if (index + 1 < num_on_deck):
            index = index + 1

    # NOTE: Key pressed up: remove & flag
    if (event.keysym == "Up"):
        student = on_deck[index]
        student.call_on(True)
        queue.take_off_deck(student)
        """
        # Some debugging info!
        print("Called on student: " + student.get_name())
        print("total times called on: ", len(student.dates_called))
        print("total times flagged: ", student.total_num_flags)
        print("dates called on: ", student.dates_called)
        """

    # NOTE: Key pressed down: remove, no flag
    if (event.keysym == "Down"):
        student = on_deck[index]
        student.call_on(False)
        queue.take_off_deck(student)
        queue.print_on_deck()
        """
        # Some debugging info!
        print("Called on student: " + student.get_name())
        print("total times called on: ", len(student.dates_called))
        print("total times flagged: ", student.total_num_flags)
        print("dates called on: ", student.dates_called)
        """
    on_deck = queue.get_on_deck()
    names.clear()
    for student in on_deck:
        names.append(student.get_name())
    a.make_labels(names, index)

class Display:
    def __init__(self):
        self.window = Tk()
        self.window.configure(bg="white")
        self.window.title("Cold Call application")
        self.window.geometry("600x100")
        self.window.bind("<Key>", key_pressed)

    def make_labels(self, names, highlighted):
        for n in range(4):
            print("i: ", n, " student: ", names[n])
            if n == index:
                bg_color = "green"
            else:
                bg_color = "white"
            Label(self.window, bg=bg_color, fg="black", text=names[n], width=0).grid(row=0, column=n)

    def show(self):
        self.window.mainloop()


if __name__ == '__main__':
    main()

a = Display()
a.make_labels(names, index)
a.show()

