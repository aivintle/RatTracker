import tkinter as tk
import numpy as np

class RatTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rat Tracker")
        self.configure(background = "black")
        self.geometry("500x300")
        self.startScreen1()

    def startScreen1(self):
        self.screen_1 = tk.Frame(self)
        self.screen_1.grid(row = 0, column = 0)
        self.screen_1.configure(background = "yellow")

        title_font = ("Lucida Sans", 20, "bold")
        self.s1_title = tk.Label(self.screen_1, text = "Rat Tracker", font = title_font, background = "yellow")
        self.s1_title.grid(row = 0, column = 1, columnspan = 2, sticky = "W", padx = 20, pady = 20)

        file_font = ("bold")
        self.s1_file_label = tk.Label(self.screen_1, text = "File: ", font = file_font, background = "yellow", padx = 20, pady = 20)
        self.s1_file_label.grid(row = 1, column = 1, sticky = "W")

        self.filepath = tk.StringVar()
        self.filepath.set("Enter a filepath.")
        self.s1_file_entry = tk.Entry(self.screen_1, textvariable = self.filepath, state = "readonly")
        self.s1_file_entry.grid(row = 1, column = 2, sticky = "W")


        self.s1_open_button = tk.Button(self.screen_1, text = "Open", command = self.open_file)
        self.s1_open_button.grid(row = 1, column = 3, padx = 20, pady = 20)        

        self.s1_help_button = tk.Button(self.screen_1, text = "Help", command = self.help)
        self.s1_help_button.grid(row = 2, column = 0, padx = 20, pady = 20)

        self.s1_next_button = tk.Button(self.screen_1, text = "Next", command = self.swap_1_to_2)
        self.s1_next_button.grid(row = 2, column = 3, padx = 20, pady = 20)

    def startScreen2(self):
        self.screen_2 = tk.Frame(self)
        self.screen_2.grid(row = 0, column = 0)
        self.previous_button = tk.Button(self.screen_2, text = "Previous", command = self.swap_2_to_1)
        self.previous_button.grid(row = 0, column = 0)
        self.previous_button = tk.Button(self.screen_2, text = "Next", command = self.swap_2_to_3)
        self.previous_button.grid(row = 0, column = 1)

    def startScreen3(self):
        self.screen_3 = tk.Frame(self)
        self.screen_3.grid(row = 0, column = 0)

        self.previous_button = tk.Button(self.screen_3, text = "Previous", command = self.swap_3_to_2)
        self.previous_button.grid(row = 0, column = 0)
        self.previous_button = tk.Button(self.screen_3, text = "Finish")
        self.previous_button.grid(row = 0, column = 1)

    def swap_1_to_2(self):
        self.screen_1.grid_forget()
        self.startScreen2()

    def swap_2_to_1(self):
        self.screen_2.grid_forget()
        self.startScreen1()

    def swap_2_to_3(self):
        self.screen_2.grid_forget()
        self.startScreen3()

    def swap_3_to_2(self):
        self.screen_3.grid_forget()
        self.startScreen2()

    def help(self):
        pass

    def open_file(self):
        pass
        

def main(): 
    app = RatTracker()
    app.mainloop()

if __name__ == '__main__':
    main()
