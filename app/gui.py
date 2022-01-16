#!/usr/bin/env python3

from controller import *

class Display:
    def __init__(self):
        self.main_window = Tk()
        self.main_window.configure(bg="white")
        self.main_window.title("Cold Call application")
        self.main_window.geometry("600x100")

        self.import_button = Button(
            self.main_window,
            text='Import roster',
            command=Controller.import_roster
        )

        self.export_button = Button(
            self.main_window,
            text='Export roster',
            command=Controller.export_roster
        )

        self.key_sequence = key_sequence.KeySequence()

        self.main_window.bind_all("<Left>", Controller.shift_index_left)
        self.main_window.bind_all("<Right>", Controller.shift_index_right)
        self.main_window.bind_all("<Up>", Controller.remove_with_flag)
        self.main_window.bind_all("<Down>", Controller.remove_without_flag)

        self.labels = [
            Label(self.main_window, bg="white", fg="black", text="", width=0) for i
            in range(NUM_ON_DECK)]

    def draw_main_screen(self, ):
        label = Label(self.main_window, bg="white", fg="black",text="Next students:", width=0)
        label.grid(row=0, column=0, padx=10, pady=20)
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