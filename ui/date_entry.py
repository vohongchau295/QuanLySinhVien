import tkinter as tk
from tkinter import ttk


class DateEntry(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.entry = ttk.Entry(self, width=15)
        self.entry.pack()

    def get(self):
        return self.entry.get()

    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

