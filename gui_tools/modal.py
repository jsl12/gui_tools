import tkinter as tk
from tkinter import ttk as ttk


class ModalInput(tk.Toplevel):
    def __init__(self, master,
                 width: int = 50, title: str = None,
                 default: str = None,
                 takefocus=True,
                 offset=(100, 100),
                 padding: int = 10,
                 *args, **kwargs):
        super().__init__(master=master,
                         takefocus=takefocus,
                         *args, **kwargs)
        self.withdraw()
        self.resizable(False, False)
        if title is not None:
            self.title(title)

        self.entry = ttk.Entry(master=self, width=width)

        self.entry.pack(expand=True, fill=tk.BOTH,
                        padx=padding, pady=(padding, 0))

        button_frame = ttk.Frame(master=self)
        button_frame.pack(side=tk.BOTTOM)

        self.ok_button = ttk.Button(master=button_frame,
                                    text='OK',
                                    command=lambda: self.destroy(set_val=True))
        self.ok_button.pack(side=tk.LEFT,
                            padx=padding, pady=padding)
        self.cancel_button = ttk.Button(master=button_frame,
                                        text='Cancel',
                                        command=lambda: self.destroy())
        self.cancel_button.pack(side=tk.LEFT,
                                padx=padding, pady=padding)

        self.set_rel_position(offset)
        self.deiconify()
        self.transient(self.master)
        self.lift()
        self.grab_set()

        if default is not None:
            self.value = default
            self.entry.delete(0, tk.END)
            self.entry.insert(0, default)

        self.entry.focus()

    def destroy(self, set_val: bool = False):
        self.grab_release()
        if set_val:
            self.value = self.entry.get()
        super().destroy()

    def set_rel_position(self, offset):
        self.update_idletasks()
        self.geometry(f'+{self.master.winfo_x() + offset[0]}+{self.master.winfo_y() + offset[1]}')