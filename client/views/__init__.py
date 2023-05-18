from functools import partial
import tkinter as tk
from tkinter import ttk

from client.globals import config
from client.views.toplevels import LoginForm, ChangePwdForm
from client.views.frames import MainFrame

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.selected_record = None
        
        # Tkinter starts...
        self.title("Please complete logging in...")
        # self.__icon = ImageTk.PhotoImage(Image.open(os.path.join(module_path, "resources", "icons", "app128.png")))
        # self.iconphoto(True, self.__icon)
        self.iconbitmap("amsdc_logo.ico")
        
        LoginForm(self, callback=self._create_ui)
        
    def _create_ui(self, apiobj):
        self.apiobj = apiobj
        
        self.title(f"AMSDC Stats Client - [{apiobj.username}]@[{apiobj.apiurl}]")
        self.state('zoomed')
        
        self.menubar = tk.Menu(self, tearoff=0)
        self.app_menu = tk.Menu(self.menubar, tearoff=0)
        self.app_menu.add_command(label=apiobj.username, state="disabled")
        self.app_menu.add_command(label="Change Password", command=partial(ChangePwdForm, self))
        self.app_menu.add_separator()
        self.app_menu.add_command(label="Exit", command=self.destroy)
        self.menubar.add_cascade(label="Application", menu=self.app_menu)
        self.config(menu=self.menubar)
        
        self.mainframe = MainFrame(self)
        self.mainframe.pack(fill=tk.BOTH, expand=True)
        
