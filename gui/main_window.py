import tkinter as tk
from tkinter import ttk, messagebox
from .graph_windows.report_window import ReportWindow
from .graph_windows.standard_graph_window import StandardGraphWindow
from .data_management.data_viewer import DataViewer

class MainWindow:
    ASCII_LOGO = """
   __     __  _____  
   \ \   / / |  __ \ 
    \ \ / /  | |  | |
     \ V /   | |  | |
      \ /    | |__| |
       V  [] |_____/       
             
                
             _,ddHHHMMMMMM?\?:\_
          .oHMMMMMMMMMMMH***9P'`"\v.
        oHMMMMMMMMMMMMMMM>  `'      -.
     .dMMMMMMMMMMMMMMMH*'|~-'          .
    ,MMMMMMMMMMMMM6>`H._,&              -.
   dMMMMMMMMMMMMMMM|  `"                  .
  H*MMMMMMMMMMMMMH&. -                     .
 d' HMM""&MMMPT'' :.                      `.-
,'  MP   `TMMM,   |:        .                -
|   #:    ? *"   : &L                        :
!   `'   /?H   ,#r `'                        :
.         ?M: HMM^<~->,o._                   :
:          `9:::'`*-``':`9MHb,|-,         '  :
.             `"''':' :_ ""!"^.  `|          :
`.                 _dbHM6_|H.      .   . '  .'
 \              _odHMMMMMMMMH,    ..  `     :
 `-             |MMMMMMMMMMMMM|            :
  `.             9MMH**#MMMMMH'           :
    -.            '     "?##"      d     :
      .                    '    ,/"    .'
       `..                          ..'
          `  .                   .-
              '`"#HHMMMMM#<>..-`
    """

    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.setup_gui()

    def setup_gui(self):
        self.master.title("Visual Data")
        
        # Set window size and position
        window_width = 800
        window_height = 600
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Set color scheme
        self.master.configure(bg='#4a86e8')  # Blue background
        
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the background
        bg_frame = tk.Frame(self.master, bg='#4a86e8')
        bg_frame.place(relwidth=1, relheight=1)

        # Add ASCII art in top left corner, slightly outset
        ascii_label = tk.Label(bg_frame, text=self.ASCII_LOGO, font=('Courier', 10), bg='#4a86e8', fg='#ffffff', justify='left')
        ascii_label.place(x=-10, y=-10)  # Slightly outset

        # Create a frame for buttons
        button_frame = tk.Frame(self.master, bg='#4a86e8')
        button_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Button style
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)

        buttons = [
            ("Upload CSV", self.app.data_handler.load_csv),
            ("View Data", self.show_data_viewer),
            ("Generate Data Report", self.show_report_window),
            ("Generate Standard Graph", self.show_standard_graph_window),
        ]

        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, style='TButton', width=30)
            btn.pack(pady=15)

    def show_data_viewer(self):
        if self.app.data_handler.data_loaded():
            DataViewer(self.master, self.app)
        else:
            messagebox.showwarning("No Data", "Please upload a CSV file first.")

    def show_report_window(self):
        if self.app.data_handler.data_loaded():
            ReportWindow(self.master, self.app)
        else:
            messagebox.showwarning("No Data", "Please upload a CSV file first.")

    def show_standard_graph_window(self):
        if self.app.data_handler.data_loaded():
            StandardGraphWindow(self.master, self.app)
        else:
            messagebox.showwarning("No Data", "Please upload a CSV file first.")