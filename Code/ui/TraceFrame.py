from ScrolledText import ScrolledText

try:
    from Code.ui.UiMot import UiMot
except ImportError:
    import sys
    sys.path.append('./Code/ui/UiMot')

try:
    from tkinter import *
except ImportError:
    from Tkinter import *


class TraceFrame(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.t = ScrolledText(self, wrap="word")
        self.t.configure(state="disabled")
        self.t.configure(height = 5)
        self.t.tag_config("in", background="yellow", foreground="red")
        self.t.tag_config("time", foreground="green")
        self.t.tag_config("curr", foreground="black")
        self.t.tag_config("out", foreground="blue")
        self.t.pack(side="top", fill="both", expand=True)


    def add_To_Trace(self, st, tag):
        self.t.configure(state=NORMAL)
        self.t.insert(INSERT, st, tag)
        self.t.configure(state="disabled")
