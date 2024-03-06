import tkinter as tk
import numpy as np
from tkinter import filedialog as fd
import os
import cv2
from PIL import Image, ImageTk

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
        self.offset_interval = 5
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
        self.s1_title.grid(row = 0, column = 1, columnspan = 2, padx = 20, pady = 20)

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

        self.s2_viewer_label = ImageLabel(self.filepath.get(), self.frame_init.get(), master = self.screen_2, background = "yellow")
        self.s2_viewer_label.grid(row = 0, column = 0, rowspan = 4, columnspan = 8, padx = 20, pady = 20, sticky = "nsew")

        self.s2_frame_changer_label = tk.Label(self.screen_2, text = "Frame Changer", background = "yellow")
        self.s2_frame_changer_label.grid(row = 4, column = 0, columnspan = 7, padx = 20, pady = 20, sticky = "ew")

        self.s2_scale_max = self.s2_viewer_label.getMax()
        
        self.s2_frame_changer_scale = tk.Scale(self.screen_2, variable = self.frame_init, background = "yellow", command = self.s2_update_num, orient = "horizontal", from_ = 1, to = self.s2_scale_max)
        self.s2_frame_changer_scale.grid(row = 5, column = 0, columnspan = 5, padx = 20, pady = 20, sticky = "ew")

        self.s2_frame_changer_entry = tk.Spinbox(self.screen_2, textvariable = self.frame_init, command = self.s2_update, from_ = 1, to = self.s2_scale_max)
        self.s2_frame_changer_entry.grid(row = 5, column = 5, columnspan = 3, padx = 20, pady = 20)

        self.s2_frame_offset_frame = tk.Frame(self.screen_2)
        self.s2_frame_offset_frame.grid(row = 0, column = 8, rowspan = 5, columnspan = 5, padx = 20, pady = 20, sticky = "nsew")
        self.s2_frame_offset_frame.configure(background = "orange")

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
        
        self.s2_top_up_button.grid(row = 1, column = 2, padx = 5, sticky = "ns")
        self.s2_bot_up_button.grid(row = 5, column = 2, padx = 5, sticky = "ns")
        self.s2_left_up_button.grid(row = 3, column = 0, pady = 5, sticky = "ew")
        self.s2_right_up_button.grid(row = 3, column = 4, pady = 5, sticky = "ew")
        self.s2_top_down_button.grid(row = 2, column = 2, padx = 5, sticky = "ns")
        self.s2_bot_down_button.grid(row = 4, column = 2, padx = 5, sticky = "ns")
        self.s2_left_down_button.grid(row = 3, column = 1, pady = 5, sticky = "ew")
        self.s2_right_down_button.grid(row = 3, column = 3, pady = 5, sticky = "ew")

        self.s2_save_button = tk.Button(self.s2_frame_offset_frame, command = self.save_Image, background = "purple")
        self.s2_save_button.grid(row = 3, column = 2, sticky = "nsew")

        self.s2_file_label = tk.Label(self.screen_2, text = self.filepath.get(), background = "yellow")
        self.s2_file_label.grid(row = 5, column = 8, columnspan = 5)
        
        self.s2_previous_button = tk.Button(self.screen_2, text = "Previous", command = self.swap_2_to_1)
        self.s2_previous_button.grid(row = 6, column = 0, padx = 20, pady = 20, sticky = "sw")
        
        self.s2_next_button = tk.Button(self.screen_2, text = "Next", command = self.swap_2_to_3)
        self.s2_next_button.grid(row = 6, column = 12, padx = 20, pady = 20, sticky = "se")

        self.screen_2.grid_rowconfigure(0, weight = 1)
        self.screen_2.grid_columnconfigure(0, weight = 1)
        try:
            self.s2_update_offsets()
        except:
            pass


    def startScreen3(self):
        self.screen_3 = tk.Frame(self)
        self.screen_3.grid(row = 0, column = 0, sticky = "nsew")
        self.screen_3.configure(background = "yellow")

        self.s3_viewer_label = ImageLabel2(self.filepath.get(), self.x, self.y, self.w, self.h, master = self.screen_3)
        self.s3_viewer_label.grid(row = 0, column = 0, rowspan = 4, columnspan = 8, padx = 20, pady = 20, sticky = "nw")

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
        
        self.s3_finish_button = tk.Button(self.screen_3, text = "Finish", command = self.save_file)
        self.s3_finish_button.grid(row = 6, column = 12, padx = 20, pady = 20)

        self.screen_3.grid_rowconfigure(0, weight = 1)
        self.screen_3.grid_columnconfigure(7, weight = 1)

    def swap_1_to_2(self):
        filepath = self.filepath.get()
        if ".mp4" in filepath:
            self.screen_1.grid_forget()
            self.startScreen2()
        else:
            raise AssertionError("No file specified")

    def swap_2_to_1(self):
        self.screen_2.grid_forget()
        self.startScreen1()

    def swap_2_to_3(self):
        try:
            self.x, self.y, self.w, self.h = self.s2_viewer_label.getBox()
        except:
            raise AssertionError("No bounding box found")
        if self.x:
            self.screen_2.grid_forget()
            self.startScreen3()

    def swap_3_to_2(self):
        self.screen_3.grid_forget()
        self.startScreen2()

    def help(self):
        pass

    def open_file(self):
        filetypes = (('mp4 files', '*.mp4'), ('Jpeg files', '*.jp*g'))
        file = fd.askopenfile(filetypes = filetypes)
        path = file.name
        source = os.path.basename(path)
        self.filepath.set(path)

    def top_Up(self):
        self.top_offset = self.top_offset - self.offset_interval
        self.s2_update_offsets()

    def top_Down(self):
        self.top_offset = self.top_offset + self.offset_interval
        self.s2_update_offsets()

    def bot_Up(self):
        self.bot_offset = self.bot_offset + self.offset_interval
        self.s2_update_offsets()

    def bot_Down(self):
        self.bot_offset = self.bot_offset - self.offset_interval
        self.s2_update_offsets()

    def left_Up(self):
        self.left_offset = self.left_offset - self.offset_interval
        self.s2_update_offsets()

    def left_Down(self):
        self.left_offset = self.left_offset + self.offset_interval
        self.s2_update_offsets()

    def right_Up(self):
        self.right_offset = self.right_offset + self.offset_interval
        self.s2_update_offsets()

    def right_Down(self):
        self.right_offset = self.right_offset - self.offset_interval
        self.s2_update_offsets()

    def save_Image(self):
        self.s2_viewer_label.capture()

    def s2_update(self):
        frameNumber = self.frame_init.get()
        self.s2_viewer_label.update(frameNumber)

    def s2_update_num(self, frameNumber):
        self.s2_viewer_label.update(int(frameNumber))

    def s2_update_offsets(self):
        self.s2_viewer_label.offsetAdjust(self.left_offset, self.top_offset, self.right_offset, self.bot_offset)
        self.s2_update()

    def save_file(self):
##        Save data in save file, raise error if file not found
        pass

    def toggle_line_ellipse(self):
        pass

    def toggle_viewer(self):
        pass

class ImageLabel(tk.Frame):
    def __init__(self, file, frameNumber, **kwargs):
        self.initConstants()
        self.initVideo(file)
        super().__init__(**kwargs)
        self.label = tk.Label(self)
        self.label.pack(fill=tk.BOTH)
        self.label.configure(background = "yellow")
        self.update(frameNumber)

    def initConstants(self):
        self.width = 450
        self.height = 300
        self.background_color = "gray"
        self.incriment = 1
        self.offset_x_min = 0
        self.offset_x_max = 0
        self.offset_y_min = 0
        self.offset_y_max = 0

    def resize(self, width, height):
        self.width = width
        self.height = height

    def update(self, frameNumber):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber - 1)
        ret, self.frame = self.cap.read(cv2.COLOR_BGR2GRAY)
        self.detectCrop()
        img = Image.fromarray(self.frame)
        resize_image = img.resize((self.width, self.height))
        self.img = ImageTk.PhotoImage(resize_image)
        self.label.configure(image = self.img)

    def nextFrame(self):
        for i in range(increment):
            ret, self.frame = self.cap.read(cv2.COLOR_BGR2GRAY)
        self.detectCrop()
        img = Image.fromarray(self.frame)
        resize_image = img.resize((self.width, self.height))
        self.img = ImageTk.PhotoImage(resize_image)
        self.label.configure(image = self.img)

    def initVideo(self, file):
        print(file)
        self.cap = cv2.VideoCapture(file)
        if not self.cap.isOpened():
            raise AssertionError("Cannot open camera")

    def getMax(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1)

    def detectCrop(self):
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        ret,thresh = cv2.threshold(gray,100,255,cv2.THRESH_TOZERO)
        gray = cv2.bitwise_not(thresh)
        ret,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)
        contour, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if contour:
            maxArea = 0
            maxContour = contour[0]
            for i in contour:
                perimeter = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02*perimeter, True)
                if len(approx) == 4:
##                    cv2.drawContours(self.frame, [i], -1, (0,255,0), 3)
                    x, y, w, h = cv2.boundingRect(approx)
                    Area = w*h
                    if (Area > maxArea):
                        maxArea = Area
                        maxContour = i
            x, y, w, h = cv2.boundingRect(cv2.approxPolyDP(maxContour, 0.02*perimeter, True))
            self.x = x + self.offset_x_min
            self.y = y + self.offset_y_min
            self.w = w + self.offset_x_max - self.offset_x_min
            self.h = h + self.offset_y_max - self.offset_y_min
            cv2.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 255), 6)

    def offsetAdjust(self, off_x_min, off_y_min, off_x_max, off_y_max):
        self.offset_x_min = off_x_min
        self.offset_x_max = off_x_max
        self.offset_y_min = off_y_min
        self.offset_y_max = off_y_max

    def getBox(self):
        return self.x, self.y, self.w, self.h

    def capture(self):
        cv2.imwrite("Save Image.png", self.frame)

class ImageLabel2(tk.Frame):
    def __init__(self, file, x, y, w, h, **kwargs):
        self.initConstants()
        self.setBox(x, y, w, h)
        self.initVideo(file)
        super().__init__(**kwargs)
        self.label = tk.Label(self)
        self.label.pack(fill=tk.BOTH)
        self.configure(background = self.background_color)
        self.update(1)

    def initConstants(self):
        self.background_color = "gray"
        self.incriment = 1

    def initVideo(self, file):
        print(file)
        self.cap = cv2.VideoCapture(file)
        if not self.cap.isOpened():
            raise AssertionError("Cannot open camera")

    def update(self, frameNumber):
        self.label.update()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frameNumber - 1)
        ret, self.frame = self.cap.read(cv2.COLOR_BGR2GRAY)
        self.crop()
        img = Image.fromarray(self.frame)
        self.img = ImageTk.PhotoImage(img)
        self.label.configure(image = self.img)

    def nextFrame(self):
        for i in range(increment):
            ret, self.frame = self.cap.read(cv2.COLOR_BGR2GRAY)
        self.crop()
        img = Image.fromarray(self.frame)
        resize_image = img.resize((self.width, self.height))
        self.img = ImageTk.PhotoImage(resize_image)
        self.label.configure(image = self.img)

    def setBox(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def crop(self):
        print(str(self.y) + ", " + str(self.y+self.h) + ", " + str(self.x) + ", " + str(self.x+self.w))
        crop = self.frame[self.y:self.y+self.h, self.x:self.x+self.w].copy()
        height, width = crop.shape[:2]
        print(width)
        ratio = height/width
        self.width = 400
        self.height = round(self.width * ratio)
        self.frame = crop
        self.frame = cv2.resize(crop, (self.width, self.height))
        height, width = self.frame.shape[:2]
        print(width)
        

def main(): 
    app = RatTracker()
    app.mainloop()

if __name__ == '__main__':
    main()
