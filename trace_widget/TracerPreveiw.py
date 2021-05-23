from tkinter import *
import threading
import time
from PIL import Image, ImageTk


class TracerPreveiw(Canvas):
    def __init__(self, root):
        super().__init__(root, highlightthickness=0, width=200, height=200, bg="white")
        self._x_line = self.create_line(0, 50, 200, 50)
        self._y_line = self.create_line(50, 0, 50, 200)
        self.background = None
        self.background_image = None
        self.running_thread = True

    def begin_trace(self, image):
        self.background_image = Image.open(image)
        self.background_image = self.background_image.resize((200, 200), resample=Image.BOX)
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background = self.create_image(0, 0, image=self.background_image, anchor=NW)
        self.tag_lower(self.background)
        threading.Thread(target=self.__thread).start()

    def __thread(self):
        for _ in range(149):
            if not self.running_thread:
                break
            try:
                self.move(self._x_line, 0, 1)
                self.move(self._y_line, 1, 0)
                print(threading.activeCount())
            except _:
                break
            time.sleep(0.1)
