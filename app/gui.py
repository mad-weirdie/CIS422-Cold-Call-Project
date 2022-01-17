#!/usr/bin/env python3

from controller import *

class Display:

    NUM_ON_DECK = 4

    def __init__(self, controller):
        self.main_window = Tk()
        self.main_window.configure(bg="white")
        self.main_window.title("Cold Call application")
        self.main_window.geometry(f'{self.main_window.winfo_screenwidth()}x70')
        self.main_window.resizable(False, False)

        self.main_window.bind_all("<Left>", controller.shift_index_left)
        self.main_window.bind_all("<Right>", controller.shift_index_right)
        self.main_window.bind_all("<Up>", controller.remove_with_flag)
        self.main_window.bind_all("<Down>", controller.remove_without_flag)

        self.main_window.wm_attributes('-transparentcolor', self.main_window['bg'])
        self.main_window.wm_attributes("-fullscreen", 1)
        self.main_window.attributes("-topmost", True)

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

        self.key_sequence = key_sequence.KeySequence()

        self.labels = [
            Label(self.main_window, bg="white", fg="black", text="", width=0) for i
            in range(self.NUM_ON_DECK)]

    def draw_main_screen(self, index, on_deck):
        names = []
        for student in on_deck:
            names.append(student.get_name())

        self.main_window.columnconfigure(0, minsize=self.main_window.winfo_screenwidth()/7)
        for i in range(self.NUM_ON_DECK):
            self.main_window.columnconfigure(i+1, minsize=self.main_window.winfo_screenwidth()/6)
        
        label = Label(self.main_window, bg="white", fg="black",text="Next students:", width=0)
        self.main_window.attributes('-topmost', True)
        label.grid(row=0, column=0, padx=10, pady=20, sticky="W")
        for n in range(self.NUM_ON_DECK):
            if n == index:
                bg_color = "black"
                fg_color = "white"
            else:
                bg_color = "white"
                fg_color = "black"
            self.labels[n].configure(bg=bg_color)
            self.labels[n].configure(fg=fg_color)
            self.labels[n].configure(text=names[n])
            self.labels[n].grid(row=0, column=(n+1), sticky="W", rowspan=1)

        self.import_button.grid(row=0, column=(self.NUM_ON_DECK+1), columnspan=1, padx=20)
        self.export_button.grid(row=0, column=(self.NUM_ON_DECK+2), columnspan=1, padx=3)