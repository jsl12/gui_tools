import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import ImageTk, Image

LOGGER = logging.getLogger(__name__)

class ImageFrame(tk.Frame):
    def __init__(self, file: Path = None, width: int = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = ttk.Label(master=self, width=width)
        self.label.pack(expand=True, fill=tk.BOTH)

        if file is not None:
            self.file = file

        self.lock = threading.Lock()
        self.label.bind('<Configure>', self.resize_event)

    @property
    def file(self) -> Path:
        return self._path

    @file.setter
    def file(self, file: Path):
        self._path: Path = file if isinstance(file, Path) else Path(file)
        LOGGER.info(f'Loading image from {self._path.name}')
        with self.lock:
            self.image_original: Image = Image.open(self._path.as_posix())
            LOGGER.info(f'Done')
        self.update_idletasks()
        self.resize(width=self.winfo_width(), height=self.winfo_height())

    def resize_event(self, event):
        if hasattr(self, 'image_original'):
            width = event.width
            height = event.height
            threading.Thread(
                target=self.resize,
                args=(width, height)
            ).start()
        else:
            LOGGER.info(f'No image loaded')

    def resize(self, width, height):
        LOGGER.info(f'Resizing to {width}x{height}')
        with self.lock:
            resized_img = self.image_original.copy()

        resized_img.thumbnail((width, height), Image.ANTIALIAS)

        photo_image = ImageTk.PhotoImage(resized_img)
        self.label.config(image=photo_image)
        self.label.image = photo_image
