import tkinter as tk
from tkinter import ttk as ttk


class ModalInput(tk.Toplevel):
    def __init__(self, master,
                 title: str = None,
                 default: str = None,
                 takefocus=True,
                 offset=(100, 100),
                 padding: int = 10,
                 # show: bool = False,
                 *args, **kwargs):
        super().__init__(master=master,
                         takefocus=takefocus,
                         *args, **kwargs)
        self.padding = padding
        self.default = default
        self.offset = offset

        self.withdraw()
        self.resizable(False, False)

        if title is not None:
            self.title(title)

        self.create_input()
        self.create_buttons()

        self.deiconify()

    def create_input(self):
        tk.Frame(master=self).pack()

    def create_buttons(self):
        button_frame = ttk.Frame(master=self)

        ok_button = ttk.Button(master=button_frame,
                               text='OK',
                               command=lambda: self.destroy(set_val=True))
        cancel_button = ttk.Button(master=button_frame,
                                   text='Cancel',
                                   command=lambda: self.destroy(set_val=False))

        ok_button.pack(side=tk.LEFT, padx=(0, int(self.padding / 2)))
        cancel_button.pack(side=tk.LEFT,
                           padx=(int(self.padding / 2), 0))

        button_frame.pack(side=tk.TOP,
                          padx=self.padding, pady=self.padding)

    def destroy(self, set_val: bool = False):
        self.grab_release()
        super().destroy()

    def deiconify(self):
        self.set_rel_position(self.offset)
        super().deiconify()
        self.transient(self.master)
        self.lift()
        self.grab_set()

    def set_rel_position(self, offset):
        self.update_idletasks()
        self.geometry(f'+{self.master.winfo_x() + offset[0]}+{self.master.winfo_y() + offset[1]}')
