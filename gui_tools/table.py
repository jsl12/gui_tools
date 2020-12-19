import logging
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from typing import Iterable, Union

import pandas as pd
from tkcalendar import DateEntry

LOGGER = logging.getLogger(__name__)

class AmountTable(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vars = {}

    @property
    def df(self):
        def get_row_series(idx):
            widgets = self.grid_slaves(row=idx)[::-1]
            key = widgets[0].get()
            var_dict = self.vars[key]
            res = pd.Series(data={'Name': var_dict['name'].get(),
                                  'Amount': float(var_dict['amount'].get()),
                                  # 'Date': var_dict['date'].get()
                                  }, name=pd.to_datetime(var_dict['date'].get()))
            return res
        return pd.DataFrame([get_row_series(idx) for idx in range(self.grid_size()[1])])


    def add_row(self, name: str, amount: float = 0., date: datetime = None):
        cols, rows = self.grid_size()
        self.vars[name] = {
            'name': tk.StringVar(value=name),
            'amount': tk.StringVar(value=f'{amount:.2f}'),
            'date': tk.StringVar(value=date.strftime('%Y-%m-%d') if date is not None else date)
        }
        self.vars[name]['amount'].trace_add('write', lambda *args: self.amount_callback(name))
        ttk.Entry(master=self,
                  textvariable=self.vars[name]['name'],
                  justify=tk.LEFT).grid(row=rows, column=0,
                                        padx=10,
                                        sticky=tk.W)
        ttk.Label(master=self, text='$').grid(row=rows, column=1,
                                              sticky=tk.E)
        ttk.Entry(master=self, width=8,
                  textvariable=self.vars[name]['amount']).grid(row=rows, column=2,
                                                               padx=(0, 10),
                                                               pady=5,
                                                               sticky=tk.E)
        DateEntry(master=self,
                  date_pattern='yyyy-MM-dd',
                  textvariable=self.vars[name]['date'],
                  ).grid(row=rows, column=3,
                         padx=(0, 10),
                         sticky=tk.E)
        RemoveButton(master=self, text='Remove').grid(row=rows, column=4,
                                                      padx=(0, 10))

        # self.vars[name]['amount'].set(f'{amount:.2f}')
        if date is not None:
            self.vars[name]['date'].set(date.strftime('%Y-%m-%d'))

    def add_rows(self, accounts: Iterable[Iterable[Union[str, float, datetime]]]):
        for args in accounts:
            self.add_row(*args)

    def get_amount(self, name: str):
        try:
            return float(self.vars[name]['amount'].get())
        except:
            return 0.0

    def amount_callback(self, name):
        LOGGER.info(f'{name}: {self.get_amount(name)}')


class RemoveButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command=self.remove)

    def remove(self):
        row = self.grid_info()['row']
        LOGGER.info(f'pos: {row}')
        for widget in self.master.grid_slaves(row=row):
            widget.grid_forget()
