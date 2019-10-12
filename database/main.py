from mongoengine import connect
from GUI import Gui, Gui_labelling
import tkinter as tk


if __name__ == '__main__':

    db = connect('ToukaAnalytics')
    #root = tk.Tk()
    root_labelling = tk.Tk()
    root_labelling.title('Labelling data for chatbot')
    root_labelling.geometry("800x500")
    #db_manager = Gui(root, db)
    training_window = Gui_labelling(root_labelling, db)
    # root.protocol("WM_DELETE_WINDOW", db_manager.kill_running_processes())
    #root.mainloop()
    root_labelling.mainloop()
