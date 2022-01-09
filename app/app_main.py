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

names = ["Alice Alison","Bob Bobbert", "Claire Clairvoyant", "Dave David"]
index = 0
def key_pressed(event):
    print(f"key pressed: {event.keysym}")
    global index
    index = (index + 1) % 4
    a.make_labels(names, index)
    # Handle key press

class Display:
    def __init__(self):
        self.window = Tk()
        self.window.configure(bg="white")
        self.window.title("Cold Call application")
        self.window.geometry("600x100")
        self.window.bind("<Key>", key_pressed)

    def make_labels(self, names, index):
        for n in range(4):
            if n == index:
                bg_color = "green"
            else:
                bg_color = "white"
            Label(self.window, bg=bg_color, fg="black", text=names[n], width=0).grid(row=0, column=n)

    def show(self):
        self.window.mainloop()

a = Display()
a.make_labels(names,index)
a.show()