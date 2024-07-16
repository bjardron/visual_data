# Use 'Agg' backend to prevent unexpected window calls
import matplotlib
matplotlib.use('Agg')

import tkinter as tk
from gui.main_window import MainWindow
from data.data_handler import DataHandler
from graphs.graph_generator import GraphGenerator
import matplotlib.pyplot as plt

try:
    plt.close('all')
except Exception as e:
    print(f"Error closing matplotlib windows: {e}")

class VisualDataApp:
    def __init__(self):
        self.root = tk.Tk()
        self.data_handler = DataHandler()
        self.graph_generator = GraphGenerator()
        self.main_window = MainWindow(self.root, self)
        self.initialize_matplotlib()

    def initialize_matplotlib(self):
        try:
            matplotlib.use('Agg')
            plt.ioff()
        except Exception as e:
            print(f"Error initializing matplotlib: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VisualDataApp()
    app.run()