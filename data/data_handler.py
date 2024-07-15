import pandas as pd
from tkinter import filedialog

class DataHandler:
    def __init__(self):
        self.data = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.data = pd.read_csv(file_path)
            return True
        return False

    def get_data(self):
        return self.data

    def get_columns(self):
        return list(self.data.columns) if self.data is not None else []

    def data_loaded(self):
        return self.data is not None