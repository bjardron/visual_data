import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


class CustomGraphWindow:
    def __init__(self, master, app):
        self.window = tk.Toplevel(master)
        self.app = app
        self.graph_options = []
        self.setup_window()

    def setup_window(self):
        self.window.title("Custom Graph Options")
        self.window.geometry("800x600")

        # Create a 2x3 grid for graph options
        for i in range(6):
            frame = ttk.LabelFrame(self.window, text=f"Graph {i+1}")
            frame.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            graph_type = ttk.Combobox(frame, values=["None", "line", "scatter", "bar", "histogram", "box", "violin"])
            graph_type.set("None")
            graph_type.pack(pady=5)

            columns = self.app.data_handler.get_columns()
            x_axis = ttk.Combobox(frame, values=columns)
            x_axis.pack(pady=5)
            y_axis = ttk.Combobox(frame, values=columns)
            y_axis.pack(pady=5)

            self.graph_options.append((graph_type, x_axis, y_axis))

        # Configure grid weights
        for i in range(2):
            self.window.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.window.grid_columnconfigure(i, weight=1)

        # Generate button
        generate_button = ttk.Button(self.window, text="Generate", command=self.generate_graphs)
        generate_button.grid(row=2, column=1, pady=20)

    def generate_graphs(self):
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Custom Graphs")

        for i, (graph_type, x_axis, y_axis) in enumerate(self.graph_options):
            if graph_type.get() != "None":
                ax = axs[i//3, i%3]
                self.app.graph_generator.generate_graph(
                    data=self.app.data_handler.get_data(),
                    graph_type=graph_type.get(),
                    x_column=x_axis.get(),
                    y_column=y_axis.get(),
                    ax=ax,
                    title=f"Graph {i+1}"
                )
            else:
                axs[i//3, i%3].axis('off')

    plt.tight_layout()
    plt.show()