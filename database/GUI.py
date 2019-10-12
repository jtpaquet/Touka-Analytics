import os
import random
import pandas as pd
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
        
        self.master = master
        self.db = db

        self.touka_dir = os.path.dirname(os.path.dirname(__file__))

        self.input_file = open(os.path.join(self.touka_dir, 'chatbot/input.from'), 'a+')
        self.reply_file = open(os.path.join(self.touka_dir, 'chatbot/reply.to'), 'a+')
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

        self.common_reply = ["oumff", "moua", "ouais ouais supère", "J'aime bien le froumage", "inks", "ceci être bruh moment", "sa ses vraies", "ceci être ma naturelle position", "oker", "gros jeu", "Fais pas ta tapet", "Criss de centriste", "Ses vraies", "Ferme ta criss de gueule", "Tayeule gros fif", "T'es juste une moumoune", "icksder"]

        # Main frame
        self.mainFrame = tk.Frame(master)
        self.mainFrame.pack(expand=True)

        # Current message
        self.messageFrame = tk.Frame(self.mainFrame)
        self.messageFrame.grid(row=0, columnspan=3, sticky='n')
        self.current_messageFrame = tk.Frame(self.messageFrame)
        self.current_messageFrame.grid(row=0, column=0)
        self.current_messageLabel= tk.Label(self.current_messageFrame, text="Message #{}".format(self.msg_n), width=20)
        self.current_messageLabel.grid(row=0, columnspan=2)
        self.current_authorLabel= tk.Label(self.current_messageFrame, text="{}:".format(self.df.loc[self.msg_n, 'author']), width=12)
        self.current_authorLabel.grid(row=1, column=0)
        self.current_message = tk.Text(self.current_messageFrame, height=5, width=30, wrap=tk.WORD)
        self.current_message.insert(tk.END, self.df.loc[self.msg_n, 'txt_msg'])
        self.current_message.grid(row=1, column=1)

        # Preceding messages
        self.preceding_messageFrame = tk.Frame(self.mainFrame)
        self.preceding_messageFrame.grid(row=3, column=0, sticky='e', padx=20, pady=20)
        self.preceding_messageLabel= tk.Label(self.preceding_messageFrame, text="Réponse à")
        self.preceding_messageLabel.grid(row=0, columnspan=3)
        self.preceding_authorLabel = []
        self.preceding_messageCanvas = []
        self.preceding_box = []
        self.preceding_var = []
        self.preceding_author_var = []
        for i in range(5):
            self.preceding_author_var.append(tk.StringVar())
            self.preceding_author_var[i].set("{}:".format(self.df.loc[self.msg_n-(i+1), 'author']))
            self.preceding_authorLabel.append(tk.Label(self.preceding_messageFrame, textvariable=self.preceding_author_var[i], width=12))
            self.preceding_authorLabel[i].grid(row=i+1, column=0)
            self.preceding_messageCanvas.append(tk.Text(self.preceding_messageFrame, height=3, width=40, wrap=tk.WORD))
            self.preceding_messageCanvas[i].insert(tk.END, self.df.loc[self.msg_n-(i+1), 'txt_msg'])
            self.preceding_messageCanvas[i].grid(row=i+1, column=1)
            self.preceding_var.append(tk.BooleanVar())
            self.preceding_box.append(tk.Checkbutton(self.preceding_messageFrame, variable = self.preceding_var[i]))
            self.preceding_box[i].grid(row=i+1, column=2)
        
        # Following messages
        self.following_messageFrame = tk.Frame(self.mainFrame)
        self.following_messageFrame.grid(row=3, column=1, sticky='w', padx=20, pady=20)
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
            self.following_authorLabel.append(tk.Label(self.following_messageFrame, textvariable=self.following_author_var[i], width=12))
            self.following_authorLabel[i].grid(row=i+1, column=0)
            self.following_messageCanvas.append(tk.Text(self.following_messageFrame, height=3, width=40, wrap=tk.WORD))
            self.following_messageCanvas[i].insert(tk.END, self.df.loc[self.msg_n+(i+1), 'txt_msg'])
            self.following_messageCanvas[i].grid(row=i+1, column=1)
            self.following_var.append(tk.BooleanVar())
            self.following_box.append(tk.Checkbutton(self.following_messageFrame, variable=self.following_var[i]))
            self.following_box[i].grid(row=i+1, column=2)

        # Common following messages
        self.common_following_messageFrame = tk.Frame(self.mainFrame)
        self.common_following_messageFrame.grid(row=3, column=2, sticky='w', padx=20, pady=20)
        self.common_following_messageLabel= tk.Label(self.common_following_messageFrame, text="Réponses courantes")
        self.common_following_messageLabel.grid(row=0, columnspan=2)
        self.common_following_messageCanvas = []
        self.common_following_box = []
        self.common_following_var = []
        self.random_common_msg = random.sample(self.common_reply, 5)
        for i in range(5):
            self.common_following_messageCanvas.append(tk.Text(self.common_following_messageFrame, height=3, width=40, wrap=tk.WORD))
            self.common_following_messageCanvas[i].insert(tk.END, self.random_common_msg[i])
            self.common_following_messageCanvas[i].grid(row=i+1, column=0)
            self.common_following_var.append(tk.BooleanVar())
            self.common_following_box.append(tk.Checkbutton(self.common_following_messageFrame, variable=self.common_following_var[i]))
            self.common_following_box[i].grid(row=i+1, column=1)

        # Other input
        self.other_msgFrame = tk.Frame(self.mainFrame)
        self.other_msgFrame.grid(row=4, columnspan=3, pady=10)
        self.other_inputFrame = tk.Frame(self.other_msgFrame)
        self.other_inputFrame.grid(row=0, column=0, padx=10)
        self.other_inputLabel= tk.Label(self.other_inputFrame, text="Autres réponses à possibles (Séparer les réponses avec ; )")
        self.other_inputLabel.grid()
        self.input_input = tk.Text(self.other_inputFrame, height=5, width=40)
        self.input_input.grid()
        # Other reply
        self.other_replyFrame = tk.Frame(self.other_msgFrame)
        self.other_replyFrame.grid(row=0, column=1, padx=10)
        self.other_replyLabel= tk.Label(self.other_replyFrame, text="Autres réponses possibles (Séparer les réponses avec ; )")
        self.other_replyLabel.grid()
        self.input_reply = tk.Text(self.other_replyFrame, height=5, width=40)
        self.input_reply.grid()
        
        # Next message
        self.buttonsFrame = tk.Frame(self.mainFrame)
        self.buttonsFrame.grid(row=5, columnspan=3, sticky='s')
        self.next_msg_Button = tk.Button(self.buttonsFrame, text='Confirmer\net passer au\nmessage #{}'.format(self.next_msg), command=self.nextMsgCmd, width=20)
        self.next_msg_Button.grid(row=0, column=0, padx=10)
        self.rand_msg_Button = tk.Button(self.buttonsFrame, text='Confirmer\net passer à un\nmessage aléatoire', command=self.randMsgCmd, width=20)
        self.rand_msg_Button.grid(row=0, column=1, padx=10)
        # Message selection
        self.selection_messageFrame = tk.Frame(self.buttonsFrame)
        self.selection_messageFrame.grid(row=0, column=2, padx=10, pady=10)
        self.selection_Label = tk.Label(self.selection_messageFrame, text="Sélection du\nprochain message")
        self.selection_Label.grid(row=0, columnspan=3)
        self.selectionLabel = tk.Label(self.selection_messageFrame, text="msg# :")
        self.selectionLabel.grid(row=1, column=0, padx=2, pady=2)
        self.selectionInput = tk.Entry(self.selection_messageFrame, width=10)
        self.selectionInput.grid(row=1, column=1, padx=2, pady=2)
        self.selectionButton = tk.Button(self.selection_messageFrame, text='Ok', command=self.selectMsgCmd)
        self.selectionButton.grid(row=1, column=2, padx=2, pady=2)
    

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
        self.update_msg()
        self.next_msg += 10
        self.next_msg_Button.config(text='Confirmer\net passer au\nmessage #{}'.format(self.next_msg))


    def randMsgCmd(self):
        self.next_msg = random.randint(5, len(self.df.index)-5)
        self.log_label()
        self.update_msg()
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

    def update_msg(self):
 
        self.msg_n = self.next_msg
        self.current_authorLabel.config(text="{}:".format(self.df.loc[self.msg_n, 'author']))
        self.current_messageLabel.config(text="Message #{}".format(self.msg_n))
        self.current_message.delete("1.0", "end")
        self.current_message.insert(tk.END, self.df.loc[self.msg_n, 'txt_msg'])
        self.random_common_msg = random.sample(self.common_reply, 5)

        for i in range(5):
            self.preceding_author_var[i].set("{}:".format(self.df.loc[self.msg_n-(i+1), 'author']))
            self.preceding_messageCanvas[i].delete("1.0", "end")
            self.preceding_messageCanvas[i].insert(tk.END, self.df.loc[self.msg_n-(i+1), 'txt_msg'])
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