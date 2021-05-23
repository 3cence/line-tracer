from tkinter import *
from TracerPreveiw import TracerPreveiw


def on_close():
    prev.running_thread = False
    root.destroy()
    exit(0)


root = Tk()
root.resizable(0, 0)
root.protocol("WM_DELETE_WINDOW", on_close)
prev = TracerPreveiw(root)
prev.pack(padx=20, pady=20)
prev.begin_trace("mappings/a.png")

root.mainloop()
prev.running_thread = False
