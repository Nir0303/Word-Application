import logging
from tkinter import *
from tkinter import ttk
import re




class GUI:
    """class for gui"""

    def __init__(self, master):
        self.definition = ttk.Label(master=root, text='  Definition:', justify="center", wraplength=500,
                                    font=("Calibre", 12), borderwidth=1, relief="sunken")
        self.sentence = ttk.Label(master=root, text='sentence completion', justify="center", wraplength=500,
                                  font=("Calibre", 11), borderwidth=1, relief="sunken")
        self.master = master
        self.master.title('Words Prediction')
        self.options = ["Auto Correction", "Auto Completion", "Sentence Completion"]
        self.v1 = StringVar()
        self.v1.set("autocorrection")
        self.button=[]
        self.word=""
        self.create_radio_button()
        self.create_labels()
        self.regex_special_chars = re.compile(r"[a-zA-Z]+")

    def create_radio_button(self):
        for i, j in enumerate(self.options):
            ttk.Radiobutton(self.master, text=j, variable=self.v1, value=j.replace(" ", "").lower()).grid(row=2,
                                                                                                          column=i)

    def create_labels(self):
        self.definition = ttk.Label(master=root, text='  Definition:', justify="center", wraplength=500,
                               font=("Calibre", 12), borderwidth=1, relief="sunken")
        self.sentence = ttk.Label(master=root, text='sentence completion', justify="center", wraplength=500,
                             font=("Calibre", 11), borderwidth=1, relief="sunken")

    def key(self,event):
        char, keysym_num = event.char, event.keysym_num
        #check for backspace
        if keysym_num != 65288:
            if self.regex_special_chars.findall(char):
                if self.word:
                    self.destroy_button()
                self.word += char
                self.create_button()
            else:
                self.word = ""
                self.destroy_button()



    def create_text_area(self, x, y):
        self.text_area = Text(master=self.master, width=x, height=y)
        self.text_area.grid(row=0, columnspan=5)
        self.text_area.bind("<Key>", self.key)

    def create_button(self):
        self.button.append(ttk.Button(master=root, text=self.word, command=self.cbc('test', self.text_area)))
        self.button[0].grid(row=1, sticky="n,e,s,w")

    def destroy_button(self):
        """function to destory buttons"""
        button_num = len(self.button) if len(self.button) <3 else 3
        for i in range(button_num):
            self.button[i].destroy()
        self.button=[]


    def cbc(self,id, tex):
        """lambda expressions created for buttons"""
        return lambda: self.callback(id, tex)

    def callback(self,word, tex):
        """ function to manage text box component"""
        s = '{}'.format(word)
        text = tex.get('1.0', 'end')


root = Tk()
app = GUI(root)
app.create_text_area(60, 10)
root.mainloop()
