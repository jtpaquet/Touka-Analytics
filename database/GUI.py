import tkinter as tk
from tkinter import ttk


class Gui:
    def __init__(self, master, db):
        
        self.db = db

        self.mainFrame = tk.Frame(master)
        self.mainFrame.pack()
        self.filterFrame = tk.Frame(self.mainFrame)
        self.filterFrame.pack()

        # Auteur
        self.authorLabel = tk.Label(self.filterFrame, text="author")
        self.authorLabel.pack()
        self.jtpButton = tk.Checkbutton(self.filterFrame, text ='jtp')
        self.jtpButton.pack()
        self.pomButton = tk.Checkbutton(self.filterFrame, text='pom')
        self.pomButton.pack()

        year = [str(y) for y in range(2012, 2020)]

        # Date
        self.dateFrameFrom = tk.Frame(self.filterFrame)
        self.dateFrameFrom.pack()
        self.dateLabel = tk.Label(self.dateFrameFrom, text="From")
        self.dateLabel.pack()
        self.year_from = ttk.Combobox(self.dateFrameFrom, values=[str(y) for y in range(2012, 2020)], width=10)
        self.year_from.pack(side=tk.LEFT)
        self.month_from = tk.ttk.Combobox(self.dateFrameFrom, values=[str(m) for m in range(1, 13)], width=5)
        self.month_from.pack(side=tk.LEFT)
        self.day_from = tk.ttk.Combobox(self.dateFrameFrom, values=[str(d) for d in range(1, 31)], width=5)
        self.day_from.pack(side=tk.LEFT)

        self.dateFrameTo = tk.Frame(self.filterFrame)
        self.dateFrameTo.pack()
        self.dateLabel = tk.Label(self.dateFrameTo, text="To")
        self.dateLabel.pack()
        self.year_to = ttk.Combobox(self.dateFrameTo, values=[str(y) for y in range(2012, 2020)], width=10)
        self.year_to.pack(side=tk.LEFT)
        self.month_to = tk.ttk.Combobox(self.dateFrameTo, values=[str(m) for m in range(1, 13)], width=5)
        self.month_to.pack(side=tk.LEFT)
        self.day_to = tk.ttk.Combobox(self.dateFrameTo, values=[str(d) for d in range(1, 31)], width=5)
        self.day_to.pack(side=tk.LEFT)

        # Include words
        self.tagFrame = tk.Frame(self.filterFrame)
        self.tagFrame.pack()
        self.tagLabel = tk.Label(self.tagFrame, text="Include words:")
        self.tagLabel.pack()
        self.tagEntry = tk.Entry(self.tagFrame)
        self.tagEntry.pack()

        # Search button
        self.searchButton = tk.Button(self.filterFrame, text='Search', command=self.searchFilter)
        self.searchButton.pack()

    def searchFilter(self):
        return 0
        
        
 
class Gui_training:
    def __init__(self, master):
                
        # Main frame
        self.mainFrame = tk.Frame(master)
        self.mainFrame.pack()
        self.messageFrame = tk.Frame(self.mainFrame)
        self.messageFrame.pack()

        # Current message
        self.current_messageFrame = tk.Frame(self.mainFrame)
        self.current_messageFrame.pack()
        self.current_messageLabel= tk.Label(self.current_messageFrame, text="Message")
        self.current_messageLabel.pack()
        self.current_messageCanvas = tk.Label(self.current_messageFrame, text="Message provenant de touka")
        self.current_messageCanvas.pack()
        
        # Following messages
        self.following_messageFrame = tk.Frame(self.mainFrame)
        self.following_messageFrame.pack()
        self.following__messageLabel= tk.Label(self.following_messageFrame, text="Réponses")
        self.following__messageLabel.pack()
        for i in range(5):
            following_messageCanvas = tk.Label(self.following_messageFrame, text="Réponse "+str(i+1))
            following_messageCanvas.pack(side=tk.LEFT)
            score_box = tk.Label(self.following_messageFrame, text="Score")
            score_box.pack(side=tk.RIGHT)
        self.no_msg_Button = tk.Button(self.following_messageFrame, text='Aucun', command=self.buttonCmd)
        self.no_msg_Button.pack()
        
        # Other messages
        self.other_messageFrame = tk.Frame(self.mainFrame)
        self.other_messageFrame.pack()
        self.other_messageLabel= tk.Label(self.other_messageFrame, text="Autre manière d'écrire le message")
        self.other_messageLabel.pack()
        self.input_messageCanvas = tk.Label(self.following_messageFrame, text="<Nouvelle manière>")
        self.input_messageCanvas.pack(side=tk.LEFT)
        
        
        # Next message
        self.next_messageFrame = tk.Frame(self.mainFrame)
        self.next_messageFrame.pack()
        self.next_messageLabel= tk.Label(self.next_messageFrame, text="Confirmation")
        self.next_messageLabel.pack()
        self.next_msg_Button = tk.Button(self.next_messageFrame, text='Confirmer et passer au message suivant', command=self.nextMsgCmd)
        self.next_msg_Button.pack()
        

    def buttonCmd(self):
        return 0
        
    def nextMsgCmd(self):
        return 0