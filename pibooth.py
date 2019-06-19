import tkinter as tk
import tkinter.ttk as ttk
from time import sleep

class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Start Page')
        label.pack(padx=10, pady=10)
        button = tk.Button(self, text='Start', command=lambda: controller.show_frame(InputForm))
        button.pack()

class InputForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Input Form')
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text='Begin!', command=lambda: controller.show_frame(CameraCapture))
        button.pack()

class CameraCapture(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Camera Capture')
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text='Print Preview', command=lambda: controller.show_frame(PrintPreview))
        button.pack()

class PrintPreview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Print Preview')
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text='Print', command=self.print_photos)
        button.pack()
        self.controller = controller

    def print_photos(self):
        print('Printing photos...')
        sleep(2)
        print('Finished!')
        sleep(2)
        self.controller.show_frame(Start)

class BoothApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Start, InputForm, CameraCapture, PrintPreview):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(Start)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


app = BoothApp()
app.mainloop()