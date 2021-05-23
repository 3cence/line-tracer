import serial
from tkinter import *


class Root(Tk):
    def mainloop(self, n=0):
        while 1:
            try:
                self.update()
                self.update_idletasks()
            except TclError:
                break
            print("Yeas")


arduino = serial.Serial("COM5", baudrate=9600, timeout=1)
root = Root()
root.title("Lights")
root.resizable(0, 0)

root.grid_columnconfigure(0, minsize=100)
root.grid_columnconfigure(1, minsize=100)
root.grid_rowconfigure(0, minsize=100)

red_btn = Button(root, text="Red", padx=20, pady=20, bg="firebrick1", activebackground="firebrick4",
                 command=lambda: arduino.write(b'1'))
red_btn.grid(row=0, column=1, sticky=N+E+W+S)
green_btn = Button(root, text="Green", padx=20, pady=20, bg="chartreuse2", activebackground="chartreuse4",
                   command=lambda: arduino.write(b'0'))
green_btn.grid(row=0, column=0, sticky=N+E+W+S)
clear_btn = Button(root, text="Reset", pady=10, bg="medium orchid", activebackground="dark violet",
                   command=lambda: arduino.write(b'2'))
clear_btn.grid(row=1, column=0, columnspan=2, sticky=N+E+W+S)

root.mainloop()
