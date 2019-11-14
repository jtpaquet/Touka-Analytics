import time
import json
import random
import os.path
import pandas as pd
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient


class Loading_screen(tk.Tk):
    def __init__(self, file_path):
        self.file_path = file_path
        tk.Tk.__init__(self)

        # Loading
        self.title('Labelling Data for Chatbot')
        self.iconbitmap(os.path.join(self.file_path, 'favicon.ico'))
        self.loadingFrame = tk.Frame(self, bg='')
        self.loadingFrame.pack(expand=True, fill=tk.BOTH)
        self.loadingImage = tk.PhotoImage(file=os.path.join(self.file_path, 'lakasse_icone256.png'))
        self.loadingCanvas = tk.Canvas(self.loadingFrame, width=self.loadingImage.width(), height=self.loadingImage.height())
        self.loadingCanvas.create_image(0, 0, image=self.loadingImage, anchor='nw')
        self.loadingCanvas.grid(row=0)

        # Connect Frame
        self.connectFrame = tk.Frame(self)
        self.connectFrame.pack(expand=True)
        self.cloudButton = tk.Button(self.connectFrame, text="Cloud DB", command= lambda: self.connect("cloud"))
        self.cloudButton.grid(row=0,column=0, padx=2, pady=2)
        self.localButton = tk.Button(self.connectFrame, text="Local DB", command= lambda: self.connect("local"))
        self.localButton.grid(row=0,column=1, padx=2, pady=2)
        self.fileButton = tk.Button(self.connectFrame, text="Fichier", command= lambda: self.connect("file"))
        self.fileButton.grid(row=0,column=2, padx=2, pady=2)
        self.center()
        self.update_idletasks()

    def updateLabel(self, n=0):
        loadinglist = ["Loading   ", "Loading.  ", "Loading.. ", "Loading..."]
        txt = loadinglist[n%len(loadinglist)]
        self.loadingLabel.config(text=txt)
        self.after(500, lambda: self.updateLabel(loadinglist.index(txt)+1))
        self.update_idletasks()

    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def connect(self, connectMethod):

        self.loadingLabel = tk.Label(self, text="Loading...", width=10)
        self.loadingLabel.pack(pady=2)
        self.update()
        self.updateLabel()

        if connectMethod == 'cloud':
            self.cloudConnect()
        elif connectMethod == 'local':
            self.localConnect()
        elif connectMethod == 'file':
            self.fileConnect()


    def cloudConnect(self):
        self.client = MongoClient("mongodb+srv://jtpaquet:pv9E9SB5gAVzKWbW@toukaanalytics-epm7v.gcp.mongodb.net/ToukaAnalytics?retryWrites=true&w=majority")
        self.db = self.client['ToukaAnalytics']
        self.launchProgram()

    
    def localConnect(self):
        self.client = MongoClient("localhost", 27017) # When offline
        self.connect(self.client)
        self.db = self.client['ToukaAnalytics']
        self.launchProgram()


    def fileConnect(self):
        self.fileDB = tk.tkFileDialog.askopenfilename(initialdir = self.file_path, title = "Select touka file", filetypes = ("json files","*.json"))
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['ToukaAnalytics']
        members = self.db['members']
        with open(self.fileDB) as f:
            self.file_data = json.load(f)
        members.insert_one(self.file_data)
        self.launchProgram()
    
    def launchProgram(self):
        training_window = Gui_labelling(self.file_path, self.db)
        self.destroy()
        training_window.mainloop()



class Gui_labelling(tk.Tk):
    def __init__(self, file_path, db):
        tk.Tk.__init__(self)

        self.file_path = file_path
        self.withdraw()

        self.title('Labelling Data for Chatbot')
        self.iconbitmap(os.path.join(file_path, 'favicon.ico'))

        self.db = db

        self.input_file = open(os.path.join(self.file_path, 'input.from'), 'a+')
        self.reply_file = open(os.path.join(self.file_path, 'reply.to'), 'a+')
        self.members = self.db['members']
        self.members = {member['name'] : member['pseudo'] for member in self.members.find()}

        self.messages = self.db['messages']

        self.data = [ [], [], [] ]
        cond = {"$and": [ {'content': {'$exists': True, '$ne': None } }, {'author': {"$in" : list(self.members.keys())} } ] }
        for msg in self.messages.find(cond):
            self.data[0].append(msg['timestamp'])
            self.data[1].append(msg['content'])
            self.data[2].append(self.members[msg['author']])
        self.df = { 'timestamp' : self.data[0], 'txt_msg' : self.data[1], 'author' : self.data[2] }
        self.df = pd.DataFrame.from_dict(self.df)
        self.df = self.df.sort_values(['timestamp'], ascending=[True])
        self.df = self.df.reset_index(drop=True)

        self.msg_n = random.randint(5, len(self.df.index)-5)
        self.next_msg = self.msg_n + 10

        self.common_reply = ["Big oumff", "oumff", "moua", "ouais ouais supère", "J'aime bien le froumage", "inks", "ceci être bruh moment", "sa ses vraies", "ceci être ma naturelle position", "oker", "gros jeu", "Fais pas ta tapet", "Criss de centriste", "Ses vraies", "Ferme ta criss de gueule", "Tayeule gros fif", "T'es juste une moumoune", "icksder"]

        # Menubar
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Cloud", command=self.center)
        self.filemenu.add_command(label="Local", command=self.center)
        self.filemenu.add_command(label="File", command=self.center)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="Connect", menu=self.filemenu)
        self.config(menu=self.menubar)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.center)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        # Main frame
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(expand=True)

        # Convo Frame
        self.convoFrame = tk.Frame(self.mainFrame)
        self.convoFrame.grid(row=0, column=0, padx=20, pady=20)

        # Other options frame
        self.other_optionFrame = tk.Frame(self.mainFrame)
        self.other_optionFrame.grid(row=0, column=1, padx=20, pady=20)

        # Preceding messages
        self.preceding_messageFrame = tk.Frame(self.convoFrame)
        self.preceding_messageFrame.grid(row=0)
        self.preceding_messageLabel= tk.Label(self.preceding_messageFrame, text="Réponse à")
        self.preceding_messageLabel.grid(row=0, columnspan=3)
        self.preceding_authorLabel = []
        self.preceding_messageCanvas = []
        self.preceding_box = []
        self.preceding_var = []
        self.preceding_author_var = []
        for i in range(5):
            self.preceding_author_var.append(tk.StringVar())
            self.preceding_author_var[i].set("{}:".format(self.df.loc[self.msg_n-(5-i), 'author']))
            self.preceding_authorLabel.append(tk.Label(self.preceding_messageFrame, textvariable=self.preceding_author_var[i], width=12))
            self.preceding_authorLabel[i].grid(row=i+1, column=0)
            self.preceding_messageCanvas.append(tk.Text(self.preceding_messageFrame, height=2, width=60, wrap=tk.WORD, font=("Verdana", 10)))
            self.preceding_messageCanvas[i].insert(tk.END, self.df.loc[self.msg_n-(5-i), 'txt_msg'])
            self.preceding_messageCanvas[i].grid(row=i+1, column=1, pady=2)
            self.preceding_var.append(tk.BooleanVar())
            self.preceding_box.append(tk.Checkbutton(self.preceding_messageFrame, variable = self.preceding_var[i]))
            self.preceding_box[i].grid(row=i+1, column=2)
        
        # Current message
        self.messageFrame = tk.Frame(self.convoFrame)
        self.messageFrame.grid(row=1, pady=20)
        self.current_messageFrame = tk.Frame(self.messageFrame)
        self.current_messageFrame.grid(row=0, column=0)
        self.current_messageLabel= tk.Label(self.current_messageFrame, text="Message #{}".format(self.msg_n), width=20)
        self.current_messageLabel.grid(row=0, columnspan=4)
        self.preceding_msg_Button = tk.Button(self.current_messageFrame, text = '<-', command= lambda: self.change_msg(n=-1))
        self.preceding_msg_Button.grid(row=1, column=0, padx=5)       
        self.current_authorLabel= tk.Label(self.current_messageFrame, text="{}:".format(self.df.loc[self.msg_n, 'author']), width=12)
        self.current_authorLabel.grid(row=1, column=1, padx=5)
        self.current_message = tk.Text(self.current_messageFrame, height=3, width=60, wrap=tk.WORD, font=("Verdana", 10))
        self.current_message.insert(tk.END, self.df.loc[self.msg_n, 'txt_msg'])
        self.current_message.grid(row=1, column=2, padx=5)
        self.following_msg_Button = tk.Button(self.current_messageFrame, text = '->', command= lambda: self.change_msg(n=1))
        self.following_msg_Button.grid(row=1, column=3, padx=5)

        # Following messages
        self.following_messageFrame = tk.Frame(self.convoFrame)
        self.following_messageFrame.grid(row=2)
        self.following_messageLabel= tk.Label(self.following_messageFrame, text="Réponses")
        self.following_messageLabel.grid(row=0, columnspan=3)
        self.following_authorLabel = [] 
        self.following_messageCanvas = []
        self.following_box = []
        self.following_var = []
        self.following_author_var = []
        for i in range(5):
            self.following_author_var.append(tk.StringVar())
            self.following_author_var[i].set("{}:".format(self.df.loc[self.msg_n+(i+1), 'author']))
            print(self.df.loc[self.msg_n+(i+1), 'author'])
            self.following_authorLabel.append(tk.Label(self.following_messageFrame, textvariable=self.following_author_var[i], width=12))
            self.following_authorLabel[i].grid(row=i+1, column=0)
            self.following_messageCanvas.append(tk.Text(self.following_messageFrame, height=2, width=60, wrap=tk.WORD, font=("Verdana", 10)))
            self.following_messageCanvas[i].insert(tk.END, self.df.loc[self.msg_n+(i+1), 'txt_msg'])
            self.following_messageCanvas[i].grid(row=i+1, column=1, pady=2)
            self.following_var.append(tk.BooleanVar())
            self.following_box.append(tk.Checkbutton(self.following_messageFrame, variable=self.following_var[i]))
            self.following_box[i].grid(row=i+1, column=2)

        # Common following messages
        self.common_following_messageFrame = tk.Frame(self.other_optionFrame)
        self.common_following_messageFrame.grid(row=0)
        self.common_following_messageLabel= tk.Label(self.common_following_messageFrame, text="Réponses courantes")
        self.common_following_messageLabel.grid(row=0, columnspan=2)
        self.common_following_messageCanvas = []
        self.common_following_box = []
        self.common_following_var = []
        self.random_common_msg = random.sample(self.common_reply, 5)
        for i in range(5):
            self.common_following_messageCanvas.append(tk.Text(self.common_following_messageFrame, height=2, width=40, wrap=tk.WORD, font=("Verdana", 10)))
            self.common_following_messageCanvas[i].insert(tk.END, self.random_common_msg[i])
            self.common_following_messageCanvas[i].grid(row=i+1, column=0, pady=2)
            self.common_following_var.append(tk.BooleanVar())
            self.common_following_box.append(tk.Checkbutton(self.common_following_messageFrame, variable=self.common_following_var[i]))
            self.common_following_box[i].grid(row=i+1, column=1)

        # Other input
        self.other_msgFrame = tk.Frame(self.other_optionFrame)
        self.other_msgFrame.grid(row=1, pady=20)
        self.other_inputFrame = tk.Frame(self.other_msgFrame)
        self.other_inputFrame.grid(row=0, column=0, pady=10)
        self.other_inputLabel= tk.Label(self.other_inputFrame, text="Autres réponses à possibles (Séparer les réponses avec ; )")
        self.other_inputLabel.grid()
        self.input_input = tk.Text(self.other_inputFrame, height=3, width=40)
        self.input_input.grid()
        # Other reply
        self.other_replyFrame = tk.Frame(self.other_msgFrame)
        self.other_replyFrame.grid(row=1, column=0, pady=10)
        self.other_replyLabel= tk.Label(self.other_replyFrame, text="Autres réponses possibles (Séparer les réponses avec ; )")
        self.other_replyLabel.grid()
        self.input_reply = tk.Text(self.other_replyFrame, height=3, width=40)
        self.input_reply.grid()
        
        # Next message
        self.buttonsFrame = tk.Frame(self.other_optionFrame)
        self.buttonsFrame.grid(row=2)
        self.next_msg_Button = tk.Button(self.buttonsFrame, text='Confirmer\net passer au\nmessage #{}'.format(self.next_msg), command=self.nextMsgCmd, width=20)
        self.next_msg_Button.grid(row=0, column=0, padx=5, pady=5)
        self.rand_msg_Button = tk.Button(self.buttonsFrame, text='Confirmer\net passer à un\nmessage aléatoire', command=self.randMsgCmd, width=20)
        self.rand_msg_Button.grid(row=1, column=0, padx=5, pady=5)
        # Message selection
        self.selection_messageFrame = tk.Frame(self.buttonsFrame)
        self.selection_messageFrame.grid(row=0, column=1, padx=5, pady=5)
        self.selection_Label = tk.Label(self.selection_messageFrame, text="Sélection du\nprochain message")
        self.selection_Label.grid(row=0, columnspan=3)
        self.selectionLabel = tk.Label(self.selection_messageFrame, text="msg# :")
        self.selectionLabel.grid(row=1, column=0, padx=2, pady=2)
        self.selectionInput = tk.Entry(self.selection_messageFrame, width=10)
        self.selectionInput.grid(row=1, column=1, padx=2, pady=2)
        self.selectionButton = tk.Button(self.selection_messageFrame, text='Ok', command=self.selectMsgCmd)
        self.selectionButton.grid(row=1, column=2, padx=2, pady=2)
        self.save_Button = tk.Button(self.buttonsFrame, text='Sauvegarder', command=self.saveProgress, width=10, height=self.rand_msg_Button.winfo_height())
        self.save_Button.grid(row=1, column=1, padx=5, pady=5)

        self.deiconify()
        self.center()


    def __del__(self):
        self.input_file.close()
        self.reply_file.close()


    def selectMsgCmd(self):
        try: 
            self.next_msg = int(self.selectionInput.get())
            self.next_msg_Button.config(text='Confirmer\net passer au\nmessage #{}'.format(self.next_msg))
        except ValueError:
            self.master.title(random.sample(['Fais pas chier', 'Press ok to ok'], 1)[0])
            self.selectionInput.delete("0","end")


    def nextMsgCmd(self):
        self.log_label()
        self.change_msg(10)
        self.next_msg += 10
        self.next_msg_Button.config(text='Confirmer\net passer au\nmessage #{}'.format(self.next_msg))


    def randMsgCmd(self):
        self.next_msg = random.randint(5, len(self.df.index)-5)
        self.log_label()
        self.change_msg(self.next_msg - self.msg_n)
        self.next_msg = self.msg_n + 10
        self.next_msg_Button.config(text='Confirmer\net passer au\nmessage #{}'.format(self.next_msg))
    

    def log_label(self):
        for i in range(len(self.following_var)):
            if self.preceding_var[i].get():
                self.reply_file.write(self.current_message.get("1.0",tk.END))
                self.input_file.write(self.preceding_messageCanvas[i].get("1.0",tk.END))
            
            if self.following_var[i].get():
                self.reply_file.write(self.following_messageCanvas[i].get("1.0",tk.END))
                self.input_file.write(self.current_message.get("1.0",tk.END))
            
            if self.common_following_var[i].get():
                self.reply_file.write(self.common_following_messageCanvas[i].get("1.0",tk.END))
                self.input_file.write(self.current_message.get("1.0",tk.END))
    
        if self.input_input.get("1.0",tk.END):
            for query in self.input_input.get("1.0", tk.END).split(';'):
                reply = self.current_message.get("1.0",tk.END).strip('\n')
                if (query != '\n'and reply != '\n'):
                    if repr(query[-2:-1]) != '\n':
                        query += '\n'
                    if repr(reply[-2:-1]) != '\n':
                        reply += '\n'
                    self.reply_file.write(reply)
                    self.input_file.write(query)

        if self.input_reply.get("1.0",tk.END):
            for reply in self.input_reply.get("1.0", tk.END).split(';'):
                query = self.current_message.get("1.0",tk.END).strip('\n')
                if (query != '\n'and reply != '\n'):
                    if repr(query[-2:-1]) != '\n':
                        query += '\n'
                    if repr(reply[-2:-1]) != '\n':
                        reply += '\n'
                    self.reply_file.write(reply)
                    self.input_file.write(query)
    
    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def saveProgress(self):
        self.input_file.close()
        self.reply_file.close()
        self.input_file = open(os.path.join(self.file_path, 'input.from'), 'a+')
        self.reply_file = open(os.path.join(self.file_path, 'reply.to'), 'a+')

    def change_msg(self, n):
        self.log_label()
        self.saveProgress()
        self.msg_n += n
        self.next_msg_Button.config(text='Confirmer\net passer au\nmessage #{}'.format(self.next_msg))
        self.current_authorLabel.config(text="{}:".format(self.df.loc[self.msg_n, 'author']))
        self.current_messageLabel.config(text="Message #{}".format(self.msg_n))
        self.current_message.delete("1.0", "end")
        self.current_message.insert(tk.END, self.df.loc[self.msg_n, 'txt_msg'])
        self.random_common_msg = random.sample(self.common_reply, 5)

        for i in range(5):
            self.preceding_author_var[i].set("{}:".format(self.df.loc[self.msg_n-(5-i), 'author']))
            print(self.df.loc[self.msg_n-(5-i), 'author'])
            self.preceding_messageCanvas[i].delete("1.0", "end")
            self.preceding_messageCanvas[i].insert(tk.END, self.df.loc[self.msg_n-(5-i), 'txt_msg'])
            self.preceding_var[i].set(False)

            self.following_author_var[i].set("{}:".format(self.df.loc[self.msg_n+(i+1), 'author']))
            self.following_messageCanvas[i].delete("1.0", "end")
            self.following_messageCanvas[i].insert(tk.END, self.df.loc[self.msg_n+(i+1), 'txt_msg'])
            self.following_var[i].set(False)

            self.common_following_messageCanvas[i].delete("1.0", "end")
            self.common_following_messageCanvas[i].insert(tk.END, self.random_common_msg[i])
            self.common_following_var[i].set(False)

        self.input_input.delete("1.0", "end")
        self.input_reply.delete("1.0", "end")
        self.update()

    def init_DB(self):
        return 0