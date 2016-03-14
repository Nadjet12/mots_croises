from Tkinter import *

from gui.ButtonFrame import ButtonFrame


class MainFrame(Frame):

    def __init__(self, master, algo, queue):

        Frame.__init__(self, master)
        self.algo = algo
        self.traceFrame = None
        self.motFrame = None
        algo.traceframe = self.traceFrame
        self.queue = queue
        self.buttonFrame = ButtonFrame(self, self.queue, self.algo, self.traceFrame, self.motFrame)


        self.buttonFrame.grid(row=0, column=0, sticky=N+E+S+W)
        print "mainfr"

    '''
    def toggle_Mot(self, bool):
        if bool:
            self.motFrame.grid(row=0, column=1,rowspan=100, sticky=N+E+S+W)
        else:
            self.motFrame.grid_forget()


    def toggle_Trace(self, bool):
        if bool:
            self.traceFrame.grid(row=2, column=0, sticky=N+E+S+W)
        else:
            self.traceFrame.grid_forget()
    '''