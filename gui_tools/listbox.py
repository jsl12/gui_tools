import tkinter as tk

class ScrolledListbox(tk.Frame):
    def __init__(self, listvariable = None, width = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_var = listvariable if listvariable is not None else tk.StringVar(value=[])
        self.list = tk.Listbox(master=self, width=width, listvariable=self.list_var)
        self.scroll = tk.Scrollbar(master=self)
        self.scroll.pack(side=tk.RIGHT, expand=False, fill=tk.BOTH)
        self.list.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.list.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.list.yview)

    @property
    def items(self):
        return self.list_var.get()

    @items.setter
    def items(self, val):
        return self.list_var.set(val)
