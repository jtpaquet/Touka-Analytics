import os.path
from pymongo import MongoClient
from GUI import Gui_labelling
import tkinter as tk

if __name__ == '__main__':

    file_path = os.path.dirname(os.path.realpath(__file__))

    # client = MongoClient("localhost", 27017) # When offline
    client = MongoClient("mongodb+srv://jtpaquet:pv9E9SB5gAVzKWbW@toukaanalytics-epm7v.gcp.mongodb.net/ToukaAnalytics?retryWrites=true&w=majority")
    db = client['ToukaAnalytics']
    root_labelling = tk.Tk()
    root_labelling.title('Labelling Data for Chatbot')
    root_labelling.iconbitmap(os.path.join(file_path, 'favicon.ico'))
    training_window = Gui_labelling(root_labelling, db)
    root_labelling.mainloop()
