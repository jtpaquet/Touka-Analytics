from mongoengine import connect
from GUI import Gui
import tkinter as tk


if __name__ == '__main__':

    db = connect('ToukaAnalytics')
    root = tk.Tk()
    db_manager = Gui(root, db)
    # root.protocol("WM_DELETE_WINDOW", db_manager.kill_running_processes())
    root.mainloop()