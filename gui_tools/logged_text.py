import logging
import queue
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

LOGGER = logging.getLogger(__name__)


class LoggedText(ScrolledText):
    def __init__(self, master, logger='', fmt=None, datefmt=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.queue = queue.Queue()
        self.handler = QueueHandler(self.queue)
        self.handler.setFormatter(
            logging.Formatter(
                fmt=fmt or '%(asctime)s [%(levelname)5s] %(name)s: %(message)s',
                datefmt=datefmt or '%H:%M:%S'
            )
        )
        logging.getLogger(logger).addHandler(self.handler)
        self.tag_config('ERROR', foreground='red')
        self.master.after(100, self.poll_queue)

    def display(self, record):
        msg = self.handler.format(record)
        self.configure(state='normal')
        self.insert(tk.END, msg + '\n', record.levelname)
        self.configure(state='disabled')
        self.yview(tk.END)

    def poll_queue(self):
        while True:
            try:
                record = self.queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.master.after(100, self.poll_queue)


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class Console(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.withdraw()
        self.output = LoggedText(master=self, width=100)
        self.output.pack(expand=True, fill=tk.BOTH)
        self.title(f'{self.master.wm_title()} Console')

    def destroy(self):
        self.withdraw()
