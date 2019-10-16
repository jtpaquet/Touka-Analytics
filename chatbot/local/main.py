import os.path
from GUI import Loading_screen
import tkinter as tk

if __name__ == '__main__':

    file_path = os.path.dirname(os.path.realpath(__file__))

    loading_window = Loading_screen(file_path)
    loading_window.mainloop()
