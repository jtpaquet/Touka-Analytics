from pymongo import MongoClient
from GUI import Gui, Gui_labelling
import tkinter as tk


if __name__ == '__main__':

    # client = MongoClient("localhost", 27017) # When offline
    client = MongoClient("mongodb+srv://jtpaquet:pv9E9SB5gAVzKWbW@toukaanalytics-epm7v.gcp.mongodb.net/ToukaAnalytics?retryWrites=true&w=majority")
    db = client['ToukaAnalytics']
    #root = tk.Tk()
    root_labelling = tk.Tk()
    root_labelling.title('Labelling Data for Chatbot')
    #db_manager = Gui(root, db)
    training_window = Gui_labelling(root_labelling, db)
    # root.protocol("WM_DELETE_WINDOW", db_manager.kill_running_processes())
    #root.mainloop()
    root_labelling.mainloop()
