import tkinter as tk
from tkinter import ttk
import pandas as pd

class DataViewer:
    def __init__(self, master, app):
        self.window = tk.Toplevel(master)
        self.app = app
        self.setup_window()

    def setup_window(self):
        self.window.title("Data Viewer")
        self.window.geometry("800x600")

        # Create a frame to hold the Treeview and scrollbars
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')

        # Create the Treeview widget
        self.tree = ttk.Treeview(frame)

        # Create vertical scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        # Create horizontal scrollbar
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=hsb.set)

        # Pack the Treeview
        self.tree.pack(expand=True, fill='both')

        self.load_data()

    def load_data(self):
        data = self.app.data_handler.get_data()
        if data is not None:
            # Clear existing data
            self.tree.delete(*self.tree.get_children())

            # Set up columns
            self.tree["columns"] = list(data.columns)
            self.tree["show"] = "headings"  # Remove the first empty column

            for col in data.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="center")

            # Insert data
            for i, row in data.iterrows():
                self.tree.insert("", "end", values=list(row))
        else:
            tk.Label(self.window, text="No data loaded").pack()