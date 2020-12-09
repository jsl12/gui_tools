import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import filedialog


class OpenFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        kwargs['padx'] = 5
        kwargs['pady'] = 5
        super().__init__(master, *args, **kwargs)
        self.rows = []
        self.columnconfigure(2, weight=1)

    def add_row(self, label_text, button_text, type = 'file', width=120):
        if type == 'file':
            func = filedialog.askopenfilename
        elif type == 'folder':
            func = filedialog.askdirectory
        else:
            func = type

        new_row = len(self.rows)
        self.rows.append([
            ttk.Label(master=self, text=label_text),
            ttk.Button(master=self, text=button_text, command=lambda *args: self.get_path(func, new_row)),
            ttk.Entry(master=self, width=width),
        ])
        self.rows[-1][0].grid(row=new_row, column=0, sticky=tk.W)
        self.rows[-1][1].grid(row=new_row, column=1, sticky=tk.W, padx=5)
        self.rows[-1][2].grid(row=new_row, column=2, sticky=(tk.W, tk.E))

    def get_row_path(self, row_num):
        try:
            return Path(self.rows[row_num][-1].get())
        except:
            pass

    def get_path(self, func, row_num):
        self.set_path(row_num,
                      func(
                          initialdir=self.get_row_path(row_num) if self.get_row_path(row_num).is_dir() else self.get_row_path(row_num).parents[0]
                      ))

    def set_path(self, row_num, path):
        path = Path(path) if not isinstance(path, Path) else path
        text_box = self.rows[row_num][2]
        text_box.delete(0, len(text_box.get()))
        text_box.insert(0, str(path))
