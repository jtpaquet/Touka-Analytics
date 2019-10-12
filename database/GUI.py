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
        
        
 
class Gui_labelling:
    def __init__(self, master, db):

        self.db = db
                
        # Main frame
        self.mainFrame = tk.Frame(master)
        self.mainFrame.pack(expand=True)
        self.messageFrame = tk.Frame(self.mainFrame)
        self.messageFrame.grid(row=0, columnspan=2, sticky='n')
        self.messageFrame.grid_configure(sticky="nsew")


        # Current message
        self.current_messageFrame = tk.Frame(self.mainFrame)
        self.current_messageFrame.grid(row=1, columnspan=2)
        self.current_messageLabel= tk.Label(self.current_messageFrame, text="Message")
        self.current_messageLabel.pack()
        self.current_message = tk.Text(self.current_messageFrame, height=5, width=60)
        self.current_message.insert(tk.END, "Message provenant de touka")
        self.current_message.pack()
        
        # Following messages
        self.following_messageFrame = tk.Frame(self.mainFrame)
        self.following_messageFrame.grid(row=3, column=0, sticky='w', padx=20, pady=20)
        self.following_messageLabel= tk.Label(self.following_messageFrame, text="Réponses")
        self.following_messageLabel.grid(row=0, columnspan=2)
        self.following_messageCanvas = []
        self.following_box = []
        self.following_var = []
        for i in range(5):
            self.following_messageCanvas.append(tk.Text(self.following_messageFrame, height=2, width=40))
            self.following_messageCanvas[i].insert(tk.END, "Réponse "+str(i+1))
            self.following_messageCanvas[i].grid(row=i+1, column=0)
            self.following_var.append(tk.IntVar())
            self.following_box.append(tk.Checkbutton(self.following_messageFrame, variable=self.following_var[i]))
            self.following_box[i].grid(row=i+1, column=1)

        # Preceding messages
        self.preceding_messageFrame = tk.Frame(self.mainFrame)
        self.preceding_messageFrame.grid(row=3, column=1, sticky='e', padx=20, pady=20)
        self.preceding_messageLabel= tk.Label(self.preceding_messageFrame, text="Réponse à")
        self.preceding_messageLabel.grid(row=0, columnspan=2)
        self.preceding_messageCanvas = []
        self.preceding_box = []
        self.preceding_var = []
        for i in range(5):
            self.preceding_messageCanvas.append(tk.Text(self.preceding_messageFrame, height=2, width=40))
            self.preceding_messageCanvas[i].insert(tk.END, "Réponse à "+str(i+1))
            self.preceding_messageCanvas[i].grid(row=i+1, column=0)
            self.preceding_var.append(tk.IntVar())
            self.preceding_box.append(tk.Checkbutton(self.preceding_messageFrame, variable = self.preceding_var[i]))
            self.preceding_box[i].grid(row=i+1, column=1)
        
        # Other messages
        self.other_messageFrame = tk.Frame(self.mainFrame)
        self.other_messageFrame.grid(row=4, columnspan=2, padx=10, pady=10)
        self.other_messageLabel= tk.Label(self.other_messageFrame, text="Autre manière d'écrire le message")
        self.other_messageLabel.grid()
        self.input_message = tk.Text(self.other_messageFrame, height=5, width=60)
        self.input_message.grid()
        
        
        # Next message
        self.next_messageFrame = tk.Frame(self.mainFrame)
        self.next_messageFrame.grid(row=5, columnspan=2, sticky='s')
        self.next_msg_Button = tk.Button(self.next_messageFrame, text='Confirmer et passer au message suivant', command=self.nextMsgCmd)
        self.next_msg_Button.pack()
        
    def nextMsgCmd(self):
        return 0