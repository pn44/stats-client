import sys
import re
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from client.globals import config
from client.constants import API_URLS
from client.controllers import APIError
from client.controllers.web import Controller
from client.helpers.auth import store_creds, read_creds, del_creds


class LoginForm(tk.Toplevel):
    def __init__(self, parent, callback=None):
        super().__init__()

        self.grab_set()
        self.transient(parent)
        # self.overrideredirect(1)

        self.title("Authorization")

        self.callback = callback

        # if getattr(sys, 'frozen', False):
            # application_path = sys._MEIPASS
        # elif __file__:
            # # application_path = os.path.dirname(__file__)
            # application_path = ""
        # # self.iconbitmap(os.path.join(application_path, "amsdc_logo.ico"))
        self.iconbitmap("amsdc_logo.ico")
        
        self.heading_l = tk.Label(self, text="Authorization")
        self.heading_l.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5)

        # Entries

        self.srv_label = tk.Label(self, text="Server URI:")
        self.srv_label.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="nsw")
        self.srv_entry = tk.StringVar(self)
        self.srv_cbox = ttk.Combobox(self,
                                     textvariable=self.srv_entry,
                                     width=28)
        self.srv_cbox["values"] = API_URLS
        self.srv_cbox.grid(
            row=1,
            column=1,
            padx=5,
            pady=5)

        self.usr_label = tk.Label(self, text="Username:")
        self.usr_label.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="nsw")
        self.usr_entry = ttk.Entry(self, width=30)
        self.usr_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5)
            
        self.usr_entry.bind("<Return>", lambda e: self.try_login())

        self.pwd_label = tk.Label(self, text="Password:")
        self.pwd_label.grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="nsw")
        self.pwd_entry = ttk.Entry(self, show="\u2022", width=30)
        self.pwd_entry.grid(
            row=3,
            column=1,
            padx=5,
            pady=5)

        self.pwd_entry.bind("<Return>", lambda e: self.try_login())
        
        
        self.otp_label = tk.Label(self, text="OTP:")
        self.otp_label.grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky="nsw")
        self.otp_entry = ttk.Entry(self, width=6)
        self.otp_entry.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky="nsw")
        self.otp_entry.bind("<Return>", lambda e: self.try_login())
        
        self.otp_label.grid_remove()
        self.otp_entry.grid_remove()
        
        self.autologin_var = tk.IntVar()
        self.autologin_chk = ttk.Checkbutton(self, text="Keep me logged in", variable=self.autologin_var)
        self.autologin_chk.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="nsw")
        self.autologin_var.set(1)
        

        self.submit = ttk.Button(self,
                                 text="Login",
                                 command=self.try_login)
        self.submit.grid(
            row=6,
            column=1,
            padx=5,
            pady=5,
            sticky="nse")
            
        if config.getboolean("login", "auto"):
            apiurl, usr, pwd = read_creds()
            
            self.srv_entry.set(apiurl)
            self.srv_cbox["state"] = "disabled"
            
            self.usr_entry.insert(tk.END, usr)
            self.usr_entry["state"] = "disabled"
            
            self.pwd_entry.insert(tk.END, pwd)
            self.pwd_entry["state"] = "disabled"
            
            # self.otp_label.grid()
            # self.otp_entry.grid()
            
            self.autologin_chk.grid_remove()
            self.autologin_var.set(0)
            
            self.submit["text"] = "Resume"
            
            self.resetbtn = ttk.Button(self,
                                 text="Turn off",
                                 command=self.del_login)
            self.resetbtn.grid(
                row=6,
                column=0,
                padx=5,
                pady=5,
                sticky="nsw")
        
    def try_login(self):
        usr = self.usr_entry.get()
        pwd = self.pwd_entry.get()
        url = self.srv_entry.get()
        if url:
            try:
                c = Controller(usr, pwd, apiurl=url)
            except APIError as e:
                if e.type == "TwoFactorCodeMissing":
                    messagebox.showinfo("Unsupported feature", 
                    "The client does not support login for accounts with two-factor authentication.")
                else:
                    messagebox.showerror("API Error", str(e))
            else:
                if self.autologin_var.get():
                    store_creds(url, usr, pwd)
                self._return_obj(c)
                self.destroy()
        else:
            messagebox.showwarning("Warning", "The API URL has not been selected.")
            
    def del_login(self):
        del_creds()
        messagebox.showinfo("Information", "Autologin has been turned "
        "off. Please note that the credentials might still be stored i"
        "n the config files and the OS's credential manager.")
        
        self.srv_cbox["state"] = "normal"
        self.usr_entry["state"] = "normal"
        self.pwd_entry["state"] = "normal"
        
        self.srv_cbox.set("")
        self.usr_entry.delete(0, tk.END)
        self.pwd_entry.delete(0, tk.END)
        self.autologin_var.set(1)
        self.submit["text"] = "Login"
        
        self.autologin_chk.grid()
        self.resetbtn.grid_remove()
            
    def _return_obj(self, obj):
        if callable(self.callback):
            self.callback.__call__(obj)


class ChangePwdForm(tk.Toplevel):
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.apiobj = parent.apiobj
        
        super().__init__()

        self.grab_set()
        self.transient(parent)
        # self.overrideredirect(1)

        self.title("Change Password")

        self.callback = callback

        # if getattr(sys, 'frozen', False):
            # application_path = sys._MEIPASS
        # else:
            # # application_path = os.path.dirname(__file__)
            # application_path = ""
        self.iconbitmap("amsdc_logo.ico")
        
        
        self.heading_l = tk.Label(self, text="Change password")
        self.heading_l.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5)

        self.pwd_label = tk.Label(self, text="Current Password:")
        self.pwd_label.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="nse")
        self.pwd_entry = ttk.Entry(self, show="\u2022", width=30)
        self.pwd_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5)

        self.pwd_entry.bind("<Return>", lambda e: self.submit_change())
        
        self.npwd_label = tk.Label(self, text="New Password:")
        self.npwd_label.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="nse")
        self.npwd_entry = ttk.Entry(self, show="\u2022", width=30)
        self.npwd_entry.grid(
            row=2,
            column=1,
            padx=5,
            pady=5)

        self.npwd_entry.bind("<Return>", lambda e: self.submit_change())
        
        self.cpwd_label = tk.Label(self, text="Confirm Password:")
        self.cpwd_label.grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky="nse")
        self.cpwd_entry = ttk.Entry(self, show="\u2022", width=30)
        self.cpwd_entry.grid(
            row=3,
            column=1,
            padx=5,
            pady=5)

        self.cpwd_entry.bind("<Return>", lambda e: self.submit_change())

        self.submit = ttk.Button(self,
                                 text="Change",
                                 command=self.submit_change)
        self.submit.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky="nse")
            
    def validate(self):
        o = self.pwd_entry.get()
        n = self.npwd_entry.get()
        c = self.cpwd_entry.get()
        e = ""
        
        if not o:
            e += "* Please enter the old password\n"
            
        if len(n)<10:
            e += "* Please enter new password more than 10 characters\n"
            
        if not c:
            e += "* Please confirm your new password\n"
        elif c != n:
            e += "* The new passwords must match\n"
        elif c == o:
            e += "* The new password cannot be the old one\n"
            
        if e:
            messagebox.showerror("Validation Error", e)
        
        return not e
        
    def submit_change(self):
        if self.validate():
            o = self.pwd_entry.get()
            n = self.npwd_entry.get()
            try:
                self.apiobj.change_pwd(o, n)
            except APIError as e:
                messagebox.showerror("API Error", str(e))
            else:
                messagebox.showinfo("Success", "Success")
                if callable(self.callback):
                    self.callback()
                self.destroy()


class PageDialogBase(tk.Toplevel, ABC):
    def __init__(self, parent, tutor=None, callback=None, *a, **kw):
        tk.Toplevel.__init__(self, parent, *a, **kw)
        
        
        self.tutor = tutor
        self.callback = callback
        
        self.transient(parent)
        
        
        self.tutor_id_label = tk.Label(self, text="# (enter this in Lektor):")
        self.tutor_id_label.grid(row=0, column=0, sticky=tk.E, padx=2, pady=2)
        self.tutor_id_entry = tk.StringVar()
        self.tutor_id__entry = ttk.Entry(self, state="readonly", textvariable=self.tutor_id_entry)
        self.tutor_id__entry.grid(row=0, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.tutor_name_label = tk.Label(self, text="Name")
        self.tutor_name_label.grid(row=1, column=0, sticky=tk.E, padx=2, pady=2)
        self.tutor_name_entry = tk.StringVar()
        self.tutor_name__entry = ttk.Entry(self, textvariable=self.tutor_name_entry)
        self.tutor_name__entry.grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)
        
        self.tutor_uid_label = tk.Label(self, text="Slug (see System Fields in Lektor)")
        self.tutor_uid_label.grid(row=2, column=0, sticky=tk.E, padx=2, pady=2)
        self.tutor_uid_entry = tk.StringVar()
        self.tutor_uid__entry = ttk.Entry(self, textvariable=self.tutor_uid_entry)
        self.tutor_uid__entry.grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)
        
        
        
        self.submit = ttk.Button(self, text="Submit")
        self.submit.grid(row=3, column=0, columnspan=2, sticky=tk.EW, padx=2, pady=2)
        
        tk.Grid.rowconfigure(self, 4, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=1)
        
        self.populate()
        # center_window_wrt(self, parent)
        
    @abstractmethod
    def populate(self):
        pass
        
    def validate(self):
        errors = ""
        id_str = self.tutor_id_entry.get()
        name = self.tutor_name_entry.get()
        uidentifier = self.tutor_uid_entry.get()
        
        if id_str:
            id = int(id_str)
        else:
            id = None
        
        if not name:
            errors += "* Please enter the name.\n"
        elif not re.fullmatch(r"[a-zA-Z0-9\- ]+", name):
            errors += f"* The name must only contain alphabets, numbers and the space character. \n"
            

        if not uidentifier:
            errors += "* Please enter the slug\n"
        elif not re.fullmatch(r"[a-z\-]+", uidentifier):
            errors += f"* The slug can only contain letters a-z, numbers 0-9, hyphen (-)\n"
        
        
        if errors:
            messagebox.showerror("Error", errors)
            
        return not errors


class AddPageForm(PageDialogBase):
    def populate(self):
        self.submit["text"] = "Add"
        self.submit["command"] = self.add
    
    def add(self):
        if self.validate():
            self.callback({
                "name": self.tutor_name_entry.get(),
                "slug": self.tutor_uid_entry.get()
            })
            self.destroy()
