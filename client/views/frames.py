import tkinter as tk
from tkinter import ttk

from client.views.widgets import ToolBar, ToolbarButton
from client.views.listboxes import PageViewFrame
from client.views.toplevels import AddPageForm


class MainFrame(ttk.Frame):
    def __init__(self, parent, *a, **kw):
        super().__init__(parent, *a, **kw)
        self.parent = parent
        self.apiobj = parent.apiobj
        
        self.toolbar = ToolBar(self)
        self.toolbar.grid(row=0, column=0, sticky='nsew')
        
        self.toolbar_new = ToolbarButton(self.toolbar, text="New Page", 
            command=lambda: AddPageForm(self, callback=self.on_page_add))
        self.toolbar_new.pack()
        
        self.toolbar_refresh = ToolbarButton(self.toolbar, text="Refresh", 
            command=self.tv_refresh)
        self.toolbar_refresh.pack()
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, anchor=tk.NW, fill='y', pady=2)
        
        self.toolbar_view = ToolbarButton(self.toolbar, text="View", command=None, state=tk.DISABLED)
        # self.toolbar_view.pack()
        self.toolbar_open = ToolbarButton(self.toolbar, text="Open", command=None, state=tk.DISABLED)
        # self.toolbar_open.pack()
        self.toolbar_edit = ToolbarButton(self.toolbar, text="Edit", command=None, state=tk.DISABLED)
        self.toolbar_edit.pack()
        self.toolbar_del = ToolbarButton(self.toolbar, text="Delete", command=None, state=tk.DISABLED)
        self.toolbar_del.pack()
        
        self.pages = PageViewFrame(self)
        self.pages.grid(row=1, column=0, sticky="nsew")
        self.tv_refresh()
        
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 1, weight=1)
        
    def on_page_add(self, js):
        self.apiobj.put_page(js)
        self.tv_refresh()
        
    def tv_refresh(self):
        self.pages.clear()
        self.pages.extend(self.apiobj.get_pages())