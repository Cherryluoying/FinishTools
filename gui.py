import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from video import VideoRecorder
from ultralytics import YOLO
import json

class AppWindow(tk.Frame):
    def __init__(self, master, config, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.config = config
        self.recorder = None
        self.create_widgets()
        #self.yolo_model = YOLO("models/yolov8_weights.pth")

    def create_widgets(self):
        self.start_button = tk.Button(self, text="开始计时", command=self.start_timing)
        self.start_button.pack(side='left',padx=10)

        self.stop_button = tk.Button(self, text="结束计时", command=self.stop_timing)
        self.stop_button.pack(side='left',padx=10)

        self.set_button = tk.Button(self, text="设置", command=self.set_endpoint)
        self.set_button.pack(side='left',padx=10)

        self.canvas = tk.Canvas(self, width=640, height=480)
        self.canvas.pack()

        self.update_video()

    def update_video(self):
        if self.recorder and self.recorder.is_recording:
            ret, frame = self.recorder.get_frame()
            if ret:
                frame = self.recorder.add_timestamp(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                self.canvas.imgtk = imgtk
        self.after(10, self.update_video)

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def start_timing(self):
        if not self.recorder:
            self.recorder = VideoRecorder(self.config)
        self.recorder.start_recording()

    def stop_timing(self):
        if self.recorder:
            self.recorder.stop_recording()
            self.recorder = None

    def set_endpoint(self):
        self.set_window = tk.Toplevel(self.master)
        self.set_window.title("设置")

        self.set_canvas = tk.Canvas(self.set_window, width=640, height=480)
        self.set_canvas.pack()

        self.set_button = tk.Button(self.set_window, text="保存", command=self.save_endpoint)
        self.set_button.pack(pady=10)

        self.set_rect = None
        self.set_canvas.bind("<Button-1>", self.draw_rectangle_start)
        self.set_canvas.bind("<B1-Motion>", self.draw_rectangle)

        self.cap = cv2.VideoCapture(0)
        self.update_set_video()

    def update_set_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.set_canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.set_canvas.imgtk = imgtk
            if self.set_rect:
                x1, y1, x2, y2 = self.set_rect
                self.set_canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=2)
        self.set_window.after(10, self.update_set_video)

    def draw_rectangle_start(self, event):
        self.rect_start = (event.x, event.y)

    def draw_rectangle(self, event):
        if self.rect_start:
            x1, y1 = self.rect_start
            x2, y2 = event.x, event.y
            self.set_rect = (x1, y1, x2, y2)
            self.set_canvas.delete("rect")
            self.set_canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=2, tag="rect")

    def save_endpoint(self):
        if self.set_rect:
            self.config["endpoint_x1"], self.config["endpoint_y1"], self.config["endpoint_x2"], self.config["endpoint_y2"] = self.set_rect
        self.cap.release()
        self.set_window.destroy()
        self.save_config()