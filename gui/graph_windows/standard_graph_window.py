import tkinter as tk
from tkinter import ttk, messagebox

class StandardGraphWindow:
    def __init__(self, master, app):
        self.window = tk.Toplevel(master)
        self.app = app
        self.setup_window()

    def setup_window(self):
        self.window.title("Standard Graph Options")
        self.window.geometry("400x300")

        if not self.app.data_handler.data_loaded():
            messagebox.showwarning("Warning", "Please upload a CSV file first.")
            self.window.destroy()
            return

        columns = self.app.data_handler.get_columns()

        tk.Label(self.window, text="Select Columns:").pack()
        self.columns_listbox = tk.Listbox(self.window, selectmode=tk.MULTIPLE, height=5)
        self.columns_listbox.pack()
        for col in columns:
            self.columns_listbox.insert(tk.END, col)

        tk.Label(self.window, text="Graph Type:").pack()
        self.graph_type_combo = ttk.Combobox(self.window, values=["bar", "histogram", "box", "correlation"])
        self.graph_type_combo.pack()

        tk.Button(self.window, text="Generate", command=self.generate).pack(pady=10)

    def generate(self):
        selected_indices = self.columns_listbox.curselection()
        selected_columns = [self.columns_listbox.get(i) for i in selected_indices]
        graph_type = self.graph_type_combo.get()
        if selected_columns and graph_type:
            data = self.app.data_handler.get_data()
            self.app.graph_generator.generate_standard_graph(data, selected_columns, graph_type)
            self.window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please select columns and graph type.")