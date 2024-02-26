import tkinter as tk
import numpy as np

class RatTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rat Tracker")
        self.configure(background = "black")
        self.geometry("500x400")
        self.startVariables()
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.startScreen1()

    def startVariables(self):
        self.filepath = tk.StringVar()
        self.savepath = tk.StringVar()
        self.filepath.set("Enter a filepath.")
        self.frame_init = tk.IntVar()
        self.frame_init.set(0)
        self.top_offset = 0
        self.left_offset = 0
        self.bot_offset = 0
        self.right_offset = 0
        self.binary_1 = tk.IntVar()
        self.binary_2 = tk.IntVar()
        self.line_ellipse_state = False
        self.viewer_state = True

    def startScreen1(self):
        self.screen_1 = tk.Frame(self)
        self.screen_1.grid(row = 0, column = 0, sticky = "nsew")
        self.screen_1.configure(background = "yellow")

        title_font = ("Lucida Sans", 20, "bold")
        self.s1_title = tk.Label(self.screen_1, text = "Rat Tracker", font = title_font, background = "yellow")
        self.s1_title.grid(row = 0, column = 1, columnspan = 2, padx = 20, pady = 20, sticky = "sw")

        file_font = ("bold")
        self.s1_file_label = tk.Label(self.screen_1, text = "File: ", font = file_font, background = "yellow", padx = 20, pady = 20)
        self.s1_file_label.grid(row = 1, column = 1)

        self.s1_file_entry = tk.Entry(self.screen_1, textvariable = self.filepath, state = "readonly")
        self.s1_file_entry.grid(row = 1, column = 2, sticky = "ew")


        self.s1_open_button = tk.Button(self.screen_1, text = "Open", command = self.open_file)
        self.s1_open_button.grid(row = 1, column = 3, padx = 20, pady = 20, sticky = "e")        

        self.s1_help_button = tk.Button(self.screen_1, text = "Help", command = self.help)
        self.s1_help_button.grid(row = 2, column = 0, padx = 20, pady = 20)

        self.s1_next_button = tk.Button(self.screen_1, text = "Next", command = self.swap_1_to_2)
        self.s1_next_button.grid(row = 2, column = 3, padx = 20, pady = 20, sticky = "se")

        self.screen_1.grid_rowconfigure(0, weight = 1)
        self.screen_1.grid_columnconfigure(2, weight = 1)

    def startScreen2(self):
        self.screen_2 = tk.Frame(self)
        self.screen_2.grid(row = 0, column = 0, sticky = "nsew")
        self.screen_2.configure(background = "yellow")

        self.s2_viewer_label = tk.Label(self.screen_2, text = "IMAGE GOES HERE", background = "yellow")
        self.s2_viewer_label.grid(row = 0, column = 0, rowspan = 4, columnspan = 8, padx = 20, pady = 20, sticky = "ew")

        self.s2_frame_changer_label = tk.Label(self.screen_2, text = "Frame Changer", background = "yellow")
        self.s2_frame_changer_label.grid(row = 4, column = 0, columnspan = 8, padx = 20, pady = 20, sticky = "ew")

        self.s2_frame_changer_scale = tk.Scale(self.screen_2, from_ = 0, to = 10, variable = self.frame_init, background = "yellow", orient = "horizontal")
        self.s2_frame_changer_scale.grid(row = 5, column = 0, columnspan = 5, padx = 20, pady = 20, sticky = "ew")

        self.s2_frame_changer_entry = tk.Entry(self.screen_2, textvariable = self.frame_init)
        self.s2_frame_changer_entry.grid(row = 5, column = 5, columnspan = 3, padx = 20, pady = 20)

        self.s2_frame_offset_frame = tk.Frame(self.screen_2)
        self.s2_frame_offset_frame.grid(row = 0, column = 8, rowspan = 5, columnspan = 5)
        self.s2_frame_offset_frame.configure(background = "yellow")

        self.s2_frame_offset_label = tk.Label(self.s2_frame_offset_frame, text = "Frame Offset", background = "yellow")
        self.s2_frame_offset_label.grid(row = 0, column = 0, columnspan = 5, padx = 5, pady = 5)

        self.s2_top_up_button = tk.Button(self.s2_frame_offset_frame, command = self.top_Up)
        self.s2_bot_up_button = tk.Button(self.s2_frame_offset_frame, command = self.bot_Up)
        self.s2_left_up_button = tk.Button(self.s2_frame_offset_frame, command = self.left_Up)
        self.s2_right_up_button = tk.Button(self.s2_frame_offset_frame, command = self.right_Up)
        self.s2_top_down_button = tk.Button(self.s2_frame_offset_frame, command = self.top_Down)
        self.s2_bot_down_button = tk.Button(self.s2_frame_offset_frame, command = self.bot_Down)
        self.s2_left_down_button = tk.Button(self.s2_frame_offset_frame, command = self.left_Down)
        self.s2_right_down_button = tk.Button(self.s2_frame_offset_frame, command = self.right_Down)
        
        self.s2_top_up_button.grid(row = 1, column = 2, padx = 5, pady = 5)
        self.s2_bot_up_button.grid(row = 5, column = 2, padx = 5, pady = 5)
        self.s2_left_up_button.grid(row = 3, column = 0, padx = 5, pady = 5)
        self.s2_right_up_button.grid(row = 3, column = 4, padx = 5, pady = 5)
        self.s2_top_down_button.grid(row = 2, column = 2, padx = 5, pady = 5)
        self.s2_bot_down_button.grid(row = 4, column = 2, padx = 5, pady = 5)
        self.s2_left_down_button.grid(row = 3, column = 1, padx = 5, pady = 5)
        self.s2_right_down_button.grid(row = 3, column = 3, padx = 5, pady = 5)

        self.s2_file_label = tk.Label(self.screen_2, text = self.filepath.get(), background = "yellow")
        self.s2_file_label.grid(row = 5, column = 8, columnspan = 5)
        
        self.s2_previous_button = tk.Button(self.screen_2, text = "Previous", command = self.swap_2_to_1)
        self.s2_previous_button.grid(row = 6, column = 0, padx = 20, pady = 20, sticky = "w")
        
        self.s2_next_button = tk.Button(self.screen_2, text = "Next", command = self.swap_2_to_3)
        self.s2_next_button.grid(row = 6, column = 12, padx = 20, pady = 20)

        self.screen_2.grid_rowconfigure(0, weight = 1)
        self.screen_2.grid_columnconfigure(0, weight = 1)

    def startScreen3(self):
        self.screen_3 = tk.Frame(self)
        self.screen_3.grid(row = 0, column = 0, sticky = "nsew")
        self.screen_3.configure(background = "yellow")

        self.s3_viewer_label = tk.Label(self.screen_3, text = "IMAGE GOES HERE", background = "yellow")
        self.s3_viewer_label.grid(row = 0, column = 0, rowspan = 4, columnspan = 8, padx = 20, pady = 20, sticky = "ew")

        self.s3_save_data_label = tk.Label(self.screen_3, text = "Save Data", background = "yellow")
        self.s3_save_data_label.grid(row = 5, column = 0, columnspan = 3, padx = 20, pady = 20, sticky = "w")

        self.s3_save_data_entry = tk.Entry(self.screen_3, textvariable = self.savepath, state = "readonly")
        self.s3_save_data_entry.grid(row = 5, column = 3, columnspan = 5, padx = 20, pady = 20, sticky = "ew")

        self.s3_save_location_button = tk.Button(self.screen_3, text = "Change", command = self.save_file)
        self.s3_save_location_button.grid(row = 5, column = 8, columnspan = 5, padx = 20, pady = 20)

        self.s3_settings_frame = tk.Frame(self.screen_3, background = "yellow")
        self.s3_settings_frame.grid(row = 0, column = 8, rowspan = 5, columnspan = 5)

        self.s3_binary_1_label = tk.Label(self.s3_settings_frame, text = "Binary 1", background = "yellow")
        self.s3_binary_2_label = tk.Label(self.s3_settings_frame, text = "Binary 2", background = "yellow")
        self.s3_line_ellipse_label = tk.Label(self.s3_settings_frame, text = "Line-Ellipse", background = "yellow")
        self.s3_viewer_label = tk.Label(self.s3_settings_frame, text = "Viewer", background = "yellow")

        self.s3_binary_1_scale = tk.Scale(self.s3_settings_frame, variable = self.binary_1, background = "yellow", orient = "horizontal")
        self.s3_binary_2_scale = tk.Scale(self.s3_settings_frame, variable = self.binary_2, background = "yellow", orient = "horizontal")

        self.s3_line_ellipse_button = tk.Button(self.s3_settings_frame, text = "OFF", command = self.toggle_line_ellipse)
        self.s3_viewer_button = tk.Button(self.s3_settings_frame, text = "ON", command = self.toggle_viewer)

        self.s3_binary_1_label.grid(row = 0, column = 0)
        self.s3_binary_1_scale.grid(row = 1, column = 0)
        self.s3_binary_2_label.grid(row = 2, column = 0)
        self.s3_binary_2_scale.grid(row = 3, column = 0)
        self.s3_line_ellipse_label.grid(row = 4, column = 0)
        self.s3_line_ellipse_button.grid(row = 5, column = 0)
        self.s3_viewer_label.grid(row = 6, column = 0)
        self.s3_viewer_button.grid(row = 7, column = 0)

        self.s3_previous_button = tk.Button(self.screen_3, text = "Previous", command = self.swap_3_to_2)
        self.s3_previous_button.grid(row = 6, column = 0, padx = 20, pady = 20)
        
        self.s3_finish_button = tk.Button(self.screen_3, text = "Finish")
        self.s3_finish_button.grid(row = 6, column = 12, padx = 20, pady = 20)

        self.screen_3.grid_rowconfigure(0, weight = 1)
        self.screen_3.grid_columnconfigure(7, weight = 1)

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

    def top_Up(self):
        self.top_offset = self.top_offset + 10
        self.s2_update()

    def top_Down(self):
        self.top_offset = self.top_offset - 10
        self.s2_update()

    def bot_Up(self):
        self.bot_offset = self.top_offset + 10
        self.s2_update()

    def bot_Down(self):
        self.bot_offset = self.top_offset - 10
        self.s2_update()

    def left_Up(self):
        self.left_offset = self.left_offset + 10
        self.s2_update()

    def left_Down(self):
        self.left_offset = self.left_offset - 10
        self.s2_update()

    def right_Up(self):
        self.right_offset = self.right_offset + 10
        self.s2_update()

    def right_Down(self):
        self.right_offset = self.right_offset - 10
        self.s2_update()

    def s2_update(self):
        pass

    def save_file(self):
        pass

    def toggle_line_ellipse(self):
        pass

    def toggle_viewer(self):
        pass

def main(): 
    app = RatTracker()
    app.mainloop()

if __name__ == '__main__':
    main()
