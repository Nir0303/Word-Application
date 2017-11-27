import logging
import tkinter as tk
from tkinter import ttk
import re

import database_helper


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
        self.v1 = tk.StringVar()
        self.v1.set("autocompletion")
        self.button = []
        self.word = ""
        self.create_radio_button()
        self.create_labels()
        self.regex_special_chars = re.compile(r"[a-zA-Z]+")

        ##Instatiate databases
        self.word_dictionary = database_helper.WordDicitionary()
        self.word_correction = database_helper.WordCorrection()
        self.word_definition = database_helper.WordDefinition()

    def create_radio_button(self):
        for i, j in enumerate(self.options):
            ttk.Radiobutton(self.master, text=j, variable=self.v1, value=j.replace(" ", "").lower()).grid(row=2,
                                                                                                          column=i)

    def create_labels(self):
        self.definition = ttk.Label(master=root, text='  Definition:', justify="center", wraplength=500,
                                    font=("Calibre", 10), borderwidth=1, relief="sunken")
        self.sentence = ttk.Label(master=root, text='sentence completion', justify="center", wraplength=500,
                                  font=("Calibre", 10), borderwidth=1, relief="sunken")

    def key(self, event):
        char, keysym_num = event.char, event.keysym_num
        # check for backspace
        if keysym_num != 65288:
            if self.regex_special_chars.findall(char):
                if self.word:
                    self.destroy_button()
                self.word += char
                self.create_button()
            else:
                self.word_dictionary.update(self.word)
                self.word = ""
                self.destroy_button()
        else:
            self.word = self.word[:-1]
            self.destroy_button()
            self.create_button()

    def create_text_area(self, x, y):
        self.text_area = tk.Text(master=self.master, width=x, height=y)
        self.text_area.grid(row=0, columnspan=5)
        self.text_area.bind("<Key>", self.key)

    def create_button(self):
        suggestions = self.get_auto_completion()

        if not suggestions:
            if self.v1.get() == "autocompletion":
                self.button.append(ttk.Button(master=root, text="add it to library", command=self.cbc(self.word)))
                self.button[0].grid(row=1, column=0, sticky="n,e,s,w")
                self.word_dictionary.insert(self.word)

            elif self.v1.get() == "autocorrection":
                suggestions = self.get_auto_correction()

        if suggestions:
            for num, word in enumerate(suggestions[:3]):
                self.button.append(ttk.Button(master=root, text=word, command=self.cbc(word[0])))
                self.button[num].grid(row=1, column=num, sticky="n,e,s,w")



    def destroy_button(self):
        """function to destory buttons"""
        button_num = len(self.button) if len(self.button) < 3 else 3
        for i in range(button_num):
            self.button[i].destroy()
        self.button = []

    def cbc(self, id):
        """lambda expressions created for buttons"""
        return lambda: self.callback(id)

    def callback(self, word):
        """ function to manage text box component"""
        s = '{}'.format(word)
        text = self.text_area.get('1.0', 'end')
        if ' ' in text:
            text = text.rsplit(' ', 1)[0]
            text += ' '
        else:
            text = ''

        self.text_area.delete('1.0', 'end')
        self.text_area.insert(tk.END, text)
        self.text_area.insert(tk.END, s)
        self.text_area.see(tk.END)

    def get_auto_completion(self):
        suggestions = self.word_dictionary.select_like(self.word)
        return suggestions

    def get_auto_correction(self):
        suggestions = self.word_dictionary.select(self.word[:-1])
        if not suggestions:
            suggestions = []
        while len(suggestions) < 3:
            word_backspace = self.word[:-1]
            vicinity_words = self.word_correction.select(self.word[-1])
            for i in vicinity_words:
                corrected_word = word_backspace + i[0]
                suggestions.extend(self.word_dictionary.select_like(corrected_word))
                if len(suggestions) > 3:
                    return suggestions
            self.word = word_backspace
        return suggestions



if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    app.create_text_area(60, 10)
    root.mainloop()
