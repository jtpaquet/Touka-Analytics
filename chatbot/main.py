import os.path
from GUI import Gui_labelling
import tkinter as tk

if __name__ == '__main__':

    file_path = os.path.dirname(os.path.realpath(__file__))

    training_window = Gui_labelling(file_path, local=False)
    training_window.mainloop()
