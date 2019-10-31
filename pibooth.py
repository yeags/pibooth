import picamera as pc
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import os

window_size = '800x480'
window_title = 'Welcome To The Moose Booth!'

class Start:
    def __init__(self, window, window_title, window_size):
        self.images = [BytesIO(), BytesIO(), BytesIO()]
        self.image_bg = Image.open('layout_resized.jpg')
        self.window = window
        self.window.title(window_title)
        self.window.config(bg='white')
        self.window.geometry(window_size)
        self.window.attributes('-fullscreen', True)
        self.frame = tk.Frame(self.window, bg='white')
        self.frame.pack(fill='y')
        self.canvas = tk.Canvas(self.frame,
                                width=800,
                                height=480,
                                bg='white')
        self.canvas.pack()
        self.window_bg = ImageTk.PhotoImage(self.image_bg)
        self.canvas.create_image(40, 0, image=self.window_bg, anchor='nw')
        self.begin_btn = tk.Button(self.frame,
                                   text='Start Photos',
                                   command=self.take_photo,
                                   height=12, width=24,
                                   relief='flat')
        self.begin_btn.place(x=300, y=150)
        
    def take_photo(self):
        for each in self.images:
            each.seek(0)
        self.camera = pc.PiCamera()
        self.camera.rotation = 0
        self.camera.resolution = (1280, 720)
        self.camera.start_preview()
        sequence = ['First Photo', 'Second Photo', 'Last Photo']
        i = 0
        self.camera.annotate_text_size = 86
        while i < 3:
            j = 3
            self.camera.annotate_text = ''
            self.camera.annotate_text = sequence[i]
            time.sleep(2)
            while j > 0:
                self.camera.annotate_text = ''
                self.camera.annotate_text = str(j)
                time.sleep(1)
                j -= 1
            self.camera.annotate_text = ''
            self.camera.capture(self.images[i], format='jpeg')
            i += 1
        self.camera.stop_preview()
        self.camera.close()
        self.preview_photostrip()
        
    def preview_photostrip(self):
        self.layout = Image.open('layout.jpg')
        paste_points = [(320, 1210), (320, 619), (320, 28)]
        pil_images = []
        for each in self.images:
            each.seek(0)
            pil_images.append(Image.open(each).crop((280,0,1000,720)).resize((563, 563)).rotate(90))
        for i in range(0, 3):
            self.layout.paste(pil_images[i], box=paste_points[i])
        layout_preview = self.layout.copy()
        layout_preview = layout_preview.rotate(-90, expand=1).resize((720, 480))
        self.preview = ImageTk.PhotoImage(layout_preview)
        self.begin_btn.destroy()
        self.canvas.destroy()
        self.preview_canvas = tk.Canvas(self.frame,
                                        width=800,
                                        height=480,
                                        bg='white')
        self.preview_canvas.pack()
        self.preview_canvas.create_image(40, 0, image=self.preview, anchor='nw')
        self.print_btn = tk.Button(self.frame, text='Print', command=self.print_photostrip,
                                   height=6, width=12, relief='flat')
        self.print_btn.pack()
        self.print_btn.place(x=795, y=5, anchor='ne')
        self.back_btn = tk.Button(self.frame, text='Start Over',
                                  command=self.startover,
                                  height=6, width=12,
                                  relief='flat')
        self.back_btn.pack()
        self.back_btn.place(x=5, y=5, anchor='nw')
        
    def startover(self):
        self.print_btn.destroy()
        self.preview_canvas.destroy()
        self.back_btn.destroy()
        self.canvas = tk.Canvas(self.frame,
                                width=800,
                                height=480,
                                bg='white')
        self.canvas.pack()
        self.window_bg = ImageTk.PhotoImage(self.image_bg)
        self.canvas.create_image(40, 0, image=self.window_bg, anchor='nw')
        self.begin_btn = tk.Button(self.frame,
                                   text='Start Photos',
                                   command=self.take_photo,
                                   height=12, width=24,
                                   relief='flat')
        self.begin_btn.place(x=300, y=150)
        
    
    def print_photostrip(self):
        self.layout.save('photostrip - ' + time.strftime('%d-%m-%Y-%H-%M-%S') + '.jpg', format='jpeg')
        self.layout.save('print_photostrip.jpg')
        os.system('lp -d CP1300 -o raw print_photostrip.jpg')
        self.print_message = messagebox.askyesno('Print', 'Successful print?')
        if self.print_message == True:
            self.startover()
        
x = Start(tk.Tk(), window_title, window_size)
x.window.mainloop()
