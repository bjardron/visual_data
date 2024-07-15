import tkinter as tk
from gui.main_window import MainWindow
from data.data_handler import DataHandler
from graphs.graph_generator import GraphGenerator
import matplotlib 

matplotlib.use ('Agg')

class VisualDataApp:
    def __init__(self):
        self.root = tk.Tk()
        self.data_handler = DataHandler()
        self.graph_generator = GraphGenerator()
        self.main_window = MainWindow(self.root, self)
        

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VisualDataApp()
    app.run()