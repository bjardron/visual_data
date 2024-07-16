import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkinter import messagebox

class ReportWindow(tk.Toplevel):
    def __init__(self, master, data_handler, graph_generator):
        super().__init__(master)
        self.data_handler = data_handler
        self.graph_generator = graph_generator
        self.title("Generate Data Report")
        self.geometry("800x600")
        self.create_widgets()

    def get_data_columns(self):
        return self.data_handler.get_columns()

    def create_widgets(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.graph_types = ["Line Plot", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot", "Text Box"]
        self.selections = []
        self.x_selections = []
        self.y_selections = []

        columns = self.get_data_columns()

        for i in range(6):
            frame = ttk.Frame(self, relief="groove", padding=5)
            frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            
            var = tk.StringVar(value="None")
            dropdown = ttk.Combobox(frame, textvariable=var, values=self.graph_types)
            dropdown.pack(pady=5)
            
            x_var = tk.StringVar(value="")
            x_dropdown = ttk.Combobox(frame, textvariable=x_var, values=columns)
            x_dropdown.pack(pady=5)
            
            y_var = tk.StringVar(value="")
            y_dropdown = ttk.Combobox(frame, textvariable=y_var, values=columns)
            y_dropdown.pack(pady=5)
            
            self.selections.append(var)
            self.x_selections.append(x_var)
            self.y_selections.append(y_var)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        generate_button = ttk.Button(button_frame, text="Generate", command=self.generate_report)
        generate_button.pack(side=tk.LEFT, padx=5)

        close_button = ttk.Button(button_frame, text="Close", command=self.destroy)
        close_button.pack(side=tk.LEFT, padx=5)

    def generate_report(self):
        selections = [(s.get(), x.get(), y.get()) for s, x, y in zip(self.selections, self.x_selections, self.y_selections) if s.get() != "None"]
        if not selections:
            messagebox.showwarning("No Selections", "Please select at least one graph type.")
            return

        fig, axs = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle("Data Report")

        for i, (selection, x_axis, y_axis) in enumerate(selections):
            if i >= 6:  # Limit to 6 graphs
                break
            ax = axs[i // 3, i % 3]
            if selection != "Text Box":
                self.graph_generator.generate_graph(
                    data=self.data_handler.get_data(),
                    graph_type=selection.lower(),
                    x_column=x_axis,
                    y_column=y_axis,
                    title=f"{selection}: {y_axis} vs {x_axis}",
                    x_label=x_axis,
                    y_label=y_axis,
                    ax=ax
                )
            else:
                text_report = self.generate_text_report()
                ax.text(0.5, 0.5, text_report, ha='center', va='center', wrap=True)
                ax.axis('off')

        # Turn off any unused subplots
        for j in range(i+1, 6):
            axs[j // 3, j % 3].axis('off')

        plt.tight_layout()
        
        # Save the figure
        try:
            fig.savefig("data_report.png")
            messagebox.showinfo("Success", "Report generated and saved as 'data_report.png'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

        # Show the figure
        plt.show()

    def generate_text_report(self):
        return self.data_handler.generate_summary()

    def generate_graph(self, graph_type, figure, x_axis, y_axis):
        self.graph_generator.generate_report_graph(figure, graph_type, x_axis, y_axis)