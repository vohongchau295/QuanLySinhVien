import tkinter as tk
from tkinter import ttk


def create_button(parent, text, command):
    return ttk.Button(
        parent,
        text=text,
        command=command
    )
