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

        tk.Label(self.window, text="Select X-axis:").pack()
        self.x_axis_var = tk.StringVar()
        self.x_axis_combo = ttk.Combobox(self.window, textvariable=self.x_axis_var, values=columns)
        self.x_axis_combo.pack()

        tk.Label(self.window, text="Select Y-axis:").pack()
        self.y_axis_var = tk.StringVar()
        self.y_axis_combo = ttk.Combobox(self.window, textvariable=self.y_axis_var, values=columns)
        self.y_axis_combo.pack()

        tk.Label(self.window, text="Graph Type:").pack()
        self.graph_types = ["Line Plot", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot"]
        self.graph_type_var = tk.StringVar()
        self.graph_type_combo = ttk.Combobox(self.window, textvariable=self.graph_type_var, values=self.graph_types)
        self.graph_type_combo.pack()

        tk.Button(self.window, text="Generate", command=self.generate).pack(pady=10)

    def generate(self):
        x_axis = self.x_axis_var.get()
        y_axis = self.y_axis_var.get()
        graph_type = self.graph_type_var.get()

        if x_axis and y_axis and graph_type:
            data = self.app.data_handler.get_data()
            self.app.graph_generator.generate_standard_graph(data, x_axis, y_axis, graph_type)
            self.window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please select X-axis, Y-axis, and graph type.")