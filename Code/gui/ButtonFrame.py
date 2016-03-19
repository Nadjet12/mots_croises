#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

        self.continueButton = Button(self, text="Continue", command=self.continueAlgo)
        self.continueButton.configure(state="disabled")
        self.continueButton.grid(row=0, column=1)


        self.advanceButton = Checkbutton(self, text="Voir les mots",
                                         variable=self.showMot, command=self.toggle_Mot)
        self.advanceButton.grid(row=0, column=2, sticky=E)
        self.traceButton = Checkbutton(self, text="Trace Algo",
                                      variable=self.showTrace, command=self.toggle_Trace)
        self.traceButton.grid(row=0, column=3, sticky=E)
        self.queue = queue
        self.algo = algo
        self.grille = algo.grille
        self.traceFrame = traceFrame
        self.motFrame = motFrame



    def play(self):
        if self.algo.isAlive():
            self.algo.stop()
        else:
            self.algo.start()

            self.master.after(100, self.process_queue)



    def process_queue(self):
        try:
            #print "try " + str(self.queue.get(0))
            result = self.queue.get(0)
            print "res :"+str(result)
            self.show(result)
        except Queue.Empty:
            #print "empty"
            self.master.after(10, self.process_queue)


    def toggle_Mot(self):
        if self.showMot.get() and self.motFrame:
            self.master.toggle_Mot(True)
            #self.motFrame.grid(row=0, column=1,rowspan=100, sticky=N+E+S+W)
        else:
            self.master.toggle_Mot(False)
            #self.c.grid_forget()

    def toggle_Trace(self):
        if self.showTrace.get() and self.traceFrame:
            self.master.toggle_Trace(True)
            #self.traceFrame.grid(row=2, column=0, sticky=N+E+S+W)
        else:
            self.master.toggle_Trace(False)
            #self.traceFrame.grid_forget()

    def show(self, result):

        if result == 'updateMot':
            self.master.updateGrille()

        elif self.algo.algo is 'AC3':
            mess = 'Non Arc-Consistant'
            if result:
                mess = 'Arc-Consistant'
            top = Toplevel()
            top.title("Resultat")

            msg = Message(top, text=mess)
            msg.pack()

        elif result:
            print "hello"
            self.continueButton.configure(state="normal")
            self.algo.wait = True
            self.grille.setResultat(result)
            print "Mots Verticaux :"
            for m in self.grille.mots_verticaux:
                m.printDomaine()
            print "Mots Horizontaux :"
            for m in self.grille.mots_horizontaux:
                m.printDomaine()
            self.master.updateGrille()

            pass
        else:
            mess = 'Pas/plus de résultat'
            top = Toplevel()
            top.title("Resultat")

            msg = Message(top, text=mess)
            msg.pack()


    def continueAlgo(self):
        self.algo.wait = False
        self.continueButton.configure(state="disabled")
        self.master.after(100, self.process_queue)
