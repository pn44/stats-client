__version__ = "0.1.0"

def main():
    from client.views import MainWindow
    import client.updater
    
    win = MainWindow()
    client.updater.main(__version__)
    win.mainloop()