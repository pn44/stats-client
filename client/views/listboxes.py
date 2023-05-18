import tkinter as tk
from tkinter import ttk
from functools import partial

class PageView(ttk.Treeview):
    def __init__(self, parent, *a, showcols=None, **kw):
        super().__init__(parent, *a, **kw)
        
        cols = ["id", "slug", "name", "views", "likes"]
        self["columns"] = cols
        self['show'] = 'headings'
        self["selectmode"] = tk.BROWSE
        
        if showcols:
            self["displaycolumns"] = showcols
        else:
            self["displaycolumns"] = ["id", "slug", "name", "views", "likes"]
        
        self.heading('id', text='#')
        self.heading('slug', text='URL Slug')
        self.heading('name', text='Page heading')
        self.heading('views', text='Views')
        self.heading('likes', text='Likes')

        self.column('id', width=40, stretch=False)
    
    def insert_queryresult(self, data):
        values=(data["id"], data["slug"], data["name"], data["views"], data["likes"])
        self.insert('', tk.END, iid="{}".format(data["id"]), values=values)
    
    def insert_queryresults(self, result):
        for assn in result:
            self.insert_queryresult(assn)
            

class TreeviewFrame(tk.Frame):
    def __init__(self, treeview, parent, *a, **kw):
        super().__init__(parent)
        
        self.treeview = treeview(self, *a, **kw)
        self.treeview.grid(row=0, column=0, sticky='nsew')
        
        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=self.yscrollbar.set)
        self.yscrollbar.grid(row=0, column=1, sticky='ns')
        
        
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        
        self.append = self.treeview.insert_queryresult
        self.extend = self.treeview.insert_queryresults
        
        self.bind = self.treeview.bind
        self.selection = self.treeview.selection
        
    def clear(self):
        self.treeview.delete(*self.treeview.get_children())


PageViewFrame = partial(TreeviewFrame, PageView)
