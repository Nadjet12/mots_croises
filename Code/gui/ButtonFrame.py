import Queue
from Tkinter import *


class ButtonFrame(Frame):

    def __init__(self, master, queue, algo=None, traceFrame=None, motFrame=None):

        Frame.__init__(self, master)
        self.showMot = IntVar()
        self.showMot.set(0)
        self.showTrace = IntVar()
        self.showTrace.set(0)


        self.playButton = Button(self, text="Play", command=self.play)
        self.playButton.grid(row=0, column=0)
        self.advanceButton = Checkbutton(self, text="Voir les mots",
                                         variable=self.showMot, command=self.toggle_Mot)
        self.advanceButton.grid(row=0, column=1, sticky=E)
        self.traceButton = Checkbutton(self, text="Trace Algo",
                                      variable=self.showTrace, command=None)
        self.traceButton.grid(row=0, column=2, sticky=E)
        self.queue = queue
        self.algo = algo
        self.grille = algo.grille
        self.traceFrame = traceFrame
        self.motFrame = motFrame
        print "buttonFra"



    def play(self):
        print "AVANT"

        self.algo.start()
        print "apres"

        self.master.after(100, self.process_queue)
        '''
        for m in self.motHori:
            m.update()
        for m in self.motVert:
            m.update()
        for m in self.motHori:
            m.printD()
        for m in self.motVert:
            m.printD()
        '''
        #self.algo.join()
        print "MOT VERT"
        for mot in self.grille.mots_verticaux:
            print mot.printDomaine()
        print "MOT HORI"
        for mot in self.grille.mots_horizontaux:
            print mot.printDomaine()


    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print msg
            # Show result of the task if needed
            #self.prog_bar.stop()
            message = "Non Arc-Consistant"
            if msg:
                self.master.updateGrille()
                message = "Arc-Consistant"

            top = Toplevel()
            top.title("Resultat")

            msg = Message(top, text=message)
            msg.pack()

        except Queue.Empty:
            self.master.after(100, self.process_queue)


    def toggle_Mot(self):
        if self.showMot.get() and self.motFrame:
            self.master.toggle_Mot(True)
            #self.motFrame.grid(row=0, column=1,rowspan=100, sticky=N+E+S+W)
        else:
            self.master.toggle_Mot(False)
            #self.c.grid_forget()
    '''
    def toggle_Trace(self):
        if self.showTrace.get() and self.traceFrame:
            self.master.toggle_Trace(True)
            #self.traceFrame.grid(row=2, column=0, sticky=N+E+S+W)
        else:
            self.master.toggle_Trace(False)
            #self.traceFrame.grid_forget()
    '''