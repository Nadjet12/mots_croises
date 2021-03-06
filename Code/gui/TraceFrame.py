from ScrolledText import ScrolledText
from Tkinter import *


class TraceFrame(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.t = ScrolledText(self, wrap="word")
        self.t.configure(background="light cyan")
        self.t.configure(height = 10)
        self.t.tag_config("in", foreground="forest green")
        self.t.tag_config("err", foreground="orange red")
        self.t.tag_config("time", foreground="sea green")
        self.t.tag_config("curr", foreground="black")
        self.t.tag_config("out", foreground="firebrick")
        self.t.pack(side="top", fill="both", expand=True)



    def add_To_Trace(self, st, tag):
        '''
        :param st: txte a afficher
        :param tag:  type de texte a afficher
        :return:
        '''
        self.t.insert(INSERT, st, tag)
        self.t.see(END)

    def clear_Trace(self):
        '''
        Efface la zone de texte
        :return:
        '''
        self.t.delete('1.0', 'end')
