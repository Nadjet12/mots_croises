#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
from Tkinter import *
from grille.Algos import Algo


class ButtonFrame(Frame):

    def __init__(self, master, queue, algo=None, traceFrame=None, motFrame=None):

        Frame.__init__(self, master)
        # variable pour l'affchage de la partie mot
        self.showMot = BooleanVar()
        self.showMot.set(False)

        # variable pour l'affchage de la partie trace
        self.showTrace = BooleanVar()
        self.showTrace.set(False)

        # bouton lancer l'algo
        self.playButton = Button(self, text="Lancer l'algo", command=self.play)
        self.playButton.grid(row=0, column=0)
        self.playButton.configure(state="disabled") # tant qu'une grille n'est pas ouverte on ne peut pas lancer l'algo

        # bouton continuer l'algo
        # s'il y a plusieurs reponse pour une grille ce bouton lance la recher de la reponse suivante
        self.continueButton = Button(self, text="Continuer l'algo", command=self.continueAlgo)
        self.continueButton.grid(row=0, column=1)
        self.continueButton.configure(state="disabled")

        # Bouton pour afficher les mots sur la droite
        self.advanceButton = Checkbutton(self, text="Voir les mots", variable=self.showMot, command=self.toggle_Mot)
        self.advanceButton.configure(state="disabled")
        self.advanceButton.grid(row=0, column=5, sticky=E)

        # remise a zéro de la grille
        self.resetButton = Button(self, text="Remise à zero", command=self.raz)
        self.resetButton.grid(row=0, column=2)
        self.resetButton.configure(state="disabled")

        #
        self.traceButton = Checkbutton(self, text="Trace algo",  variable=self.showTrace, command=self.toggle_Trace)
        self.traceButton.grid(row=0, column=3, sticky=E)


        self.cleartraceButton = Button(self, text="Clear Trace", command=self.clearTrace)
        self.cleartraceButton.configure(state="disabled")
        self.cleartraceButton .grid(row=0, column=4, sticky=E)


        self.queue = queue
        self.algo = algo
        self.traceFrame = traceFrame
        self.motFrame = motFrame



    def play(self):
        '''
        Lance l'algo de resolution de mots croisés
        Si une instance est déja en train de tourner il l'arrete et lance une nouvelle instance
        :return: None
        '''
        self.resetButton.configure(state="normal")
        if self.algo.hasRun:
            self.algo.stop()
            self.raz()
            self.algo = Algo(queue=self.queue, grille=self.algo.grille, traceframe=self.traceFrame, algoName=self.algo.algoName, heuristique=self.algo.heur)

        self.algo.start()
        self.after(1000, self.process_queue)
        self.master.send_To_Trace("nombre de mot sur la grille :" + str(len(self.algo.grille.mots_horizontaux + self.algo.grille.mots_verticaux))+"\n", "curr")
        self.master.send_To_Trace("nombre de mot dans les Domaines :" + str(self.algo.grille.get_Domaines_Sizes())+"\n", "curr")
        self.resetButton.configure(state="disabled")

    def raz(self):
        '''
        Remet la grille a zéro
        :return: None
        '''
        self.master.Ggrille(self.algo.grille.filePath)
        self.resetButton.configure(state="disabled")

    def process_queue(self):
        '''
        lance la procedure de la queue d'evenement de l'algo
        :return: None
        '''
        try:
            result = self.queue.get(0)
            self.show(result)
        except Queue.Empty:
            self.after(1000, self.process_queue)

    def toggle_Mot(self):
        '''
        Affiche sur la droite des mots de la grille
        :return: None
        '''
        if self.showMot.get() and self.motFrame:
            self.master.toggle_Mot(True)
        else:
            self.master.toggle_Mot(False)

    def toggle_Trace(self):
        '''
        Affiche en ba une Trace de l'algo
        :return:
        '''
        if self.showTrace.get() and self.traceFrame:
            self.master.toggle_Trace(True)
            self.cleartraceButton.configure(state="normal")
        else:
            self.master.toggle_Trace(False)
            self.cleartraceButton.configure(state="disabled")

    def clearTrace(self):
        '''
        Efface la console de Trace
        :return:
        '''
        if self.traceFrame:
            self.master.clearTrace()

    def show(self, result):
        '''

        :param result: Résultat de l'algo
        :return:
        '''

        if self.algo.algoName is 'AC3':
            mess = 'Non Arc-Consistant'
            if result:
                mess = 'Arc-Consistant'
                self.master.updateGrille()
            top = Toplevel()
            top.title("Resultat de l'Arc-Consistance")

            msg = Message(top, text=mess, width=150)
            msg.pack()
            self.algo.stop()
        elif isinstance(result, tuple):
            if result[0] is 'AC3':
                self.master.updateGrille()
        elif result:
            self.continueButton.configure(state="normal")
            self.algo.grille.setResultat(result)
            self.master.updateGrille()
            for m in self.algo.grille.mots_horizontaux + self.algo.grille.mots_verticaux:
                self.master.send_To_Trace(str(m)+'\n', "curr")
        else:
            self.continueButton.configure(state="disabled")
            mess = 'Pas/plus de résultat'
            top = Toplevel()
            top.title("Resultat")
            msg = Message(top, text=mess)
            msg.pack()
            self.algo.stop()
        self.after(1000, self.process_queue)


    def continueAlgo(self):
        '''
        Continue la resolution de la grille pour un nouveau resultat
        :return:
        '''
        self.algo.resume()
        self.continueButton.configure(state="disabled")
        self.after(1000, self.process_queue)

    def enableMot(self, bool):
        '''
        Autorise la selection des bouton mot et lancement de l'algo
        :param bool:
        :return:
        '''
        if bool:
            self.playButton.configure(state="normal")
            self.advanceButton.configure(state="normal")
        else:
            self.advanceButton.configure(state="disabled")
            self.playButton.configure(state="disabled")