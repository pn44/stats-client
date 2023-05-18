import tkinter as tk
from tkinter import ttk

class ToolBar(tk.Frame):
    def __init__(self, parent, *a, bd=1, relief = tk.RAISED, **kw):
        self.parent = parent
        super().__init__(self.parent, *a, bd=bd, relief=relief, **kw)

        self.menus = {}

    def set_menu(self, name, text, menu):
        if name not in self.menus:
            mb = ttk.Menubutton(self)
            mb.pack(side=tk.LEFT, anchor=tk.NW)
            self.menus[name] = mb
        self.menus[name]["text"] = text
        self.menus[name]["menu"] = menu

    def set_button(self, name, text, command=None, state=tk.NORMAL):
        if name not in self.menus:
            mb = tk.Button(self, bd=0, relief=tk.FLAT)
            mb.pack(side=tk.LEFT, anchor=tk.NW)
            self.menus[name] = mb
        self.menus[name]["text"] = text
        self.menus[name]["command"] = command
        self.menus[name]["state"] = state


class MultiStatusBar(ttk.Frame):
    def __init__(self, master, **kw):
        ttk.Frame.__init__(self, master, **kw)
        self.labels = {}

    def set_label(self, name, text='', side='left', width=0):
        if name not in self.labels:
            label = ttk.Label(self, borderwidth=0, anchor='w')
            label.pack(side=side, pady=0, padx=4)
            self.labels[name] = label
        else:
            label = self.labels[name]
        if width != 0:
            label.config(width=width)
        label.config(text=text)


class ToolbarWidget:
    def _bind_hovers(self):
        self.default_background = self['background']
        self.config(relief=tk.FLAT, bd=0, activebackground="#d8e6f2")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if self['state'] == tk.NORMAL:
            self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.default_background
        
    def pack(self, side=tk.LEFT, anchor=tk.NW, padx=2, **kw):
        super().pack(side=side, anchor=anchor, padx=padx, **kw)
        
class ToolbarButton(ToolbarWidget, tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, relief=tk.FLAT, bd=0, activebackground="#d8e6f2", **kw)
        self.default_background = self['background']
        self._bind_hovers()
        
class ToolbarMenubutton(ToolbarWidget, tk.Menubutton):
    def __init__(self, master, **kw):
        tk.Menubutton.__init__(self, master, **kw)
        self._bind_hovers()
        
        
#https://stackoverflow.com/questions/59763822/show-combobox-drop-down-while-editing-text-using-tkinter

class DropdownCombobox(ttk.Combobox):
    def _tk(self, cls, parent):
        obj = cls(parent)
        obj.destroy()
        if cls is tk.Toplevel:
            obj._w = self.tk.call('ttk::combobox::PopdownWindow', self)
        else:
            obj._w = '{}.{}'.format(parent._w, 'f.l')
        return obj

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.popdown = self._tk(tk.Toplevel, parent)
        self.listbox = self._tk(tk.Listbox, self.popdown)

        self.bind("<KeyPress>", self.on_keypress, '+')
        self.listbox.bind("<Up>", self.on_keypress)

    def on_keypress(self, event):
        if event.widget == self:
            state = self.popdown.state()

            if state == 'withdrawn' \
                    and event.keysym not in ['BackSpace', 'Up']:
                self.event_generate('<Button-1>')
                self.after(0, self.focus_set)

            if event.keysym == 'Down':
                self.after(0, self.listbox.focus_set)

        else:  # self.listbox
            curselection = self.listbox.curselection()

            if event.keysym == 'Up' and (len(curselection) == 0 or curselection[0] == 0):
                self.popdown.withdraw()