import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from reportlab.pdfgen import canvas as rlcanvas
from reportlab.lib.pagesizes import letter
import io

class ReportWindow(tk.Toplevel):
    def __init__(self, master, data_handler, graph_generator):
        super().__init__(master)
        self.data_handler = data_handler
        self.graph_generator = graph_generator
        self.title("Generate Data Report")
        self.geometry("800x600")
        self.create_widgets()

    def get_data_columns(self):
        return self.data_handler.get_column_names()

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
        try:
            selections = [(s.get(), x.get(), y.get()) for s, x, y in zip(self.selections, self.x_selections, self.y_selections) if s.get() != "None"]
            if not selections:
                raise ValueError("No graph types selected")

            pdf_buffer = io.BytesIO()
            pdf = rlcanvas.Canvas(pdf_buffer, pagesize=letter)

            for i, (selection, x_axis, y_axis) in enumerate(selections):
                if selection == "Text Box":
                    text_report = self.generate_text_report()
                    pdf.drawString(100, 700 - i*100, text_report)
                else:
                    fig = Figure(figsize=(5, 4), dpi=100)
                    self.generate_graph(selection, fig, x_axis, y_axis)
                    img_data = io.BytesIO()
                    fig.savefig(img_data, format='png')
                    img_data.seek(0)
                    pdf.drawImage(img_data, 100, 700 - i*200, width=400, height=300)

            pdf.save()
            
            with open("report.pdf", "wb") as f:
                f.write(pdf_buffer.getvalue())
            
            messagebox.showinfo("Success", "Report generated and saved as 'report.pdf'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def generate_text_report(self):
        return self.data_handler.generate_summary()

    def generate_graph(self, graph_type, figure, x_axis, y_axis):
        self.graph_generator.generate_report_graph(figure, graph_type, x_axis, y_axis)