from mongoengine import connect
from GUI import Gui, Gui_training
import tkinter as tk


if __name__ == '__main__':

    db = connect('ToukaAnalytics')
    #root = tk.Tk()
    root_training = tk.Tk()
    #db_manager = Gui(root, db)
    training_window = Gui_training(root_training, db)
    # root.protocol("WM_DELETE_WINDOW", db_manager.kill_running_processes())
    #root.mainloop()
    root_training.mainloop()
