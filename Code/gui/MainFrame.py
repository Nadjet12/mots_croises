import tkFont
from Tkinter import *

from gui.ButtonFrame import ButtonFrame
from gui.Case import Case
from gui.GMot import GMot
from gui.GrilleFrame import GrilleFrame
from gui.MotFrame import MotFrame
from gui.TraceFrame import TraceFrame


class MainFrame(Frame):

    def __init__(self, master, algo, queue):

        Frame.__init__(self, master)
        self.algo = algo
        print self.algo
        self.traceFrame = TraceFrame(self)
        self.motFrame = MotFrame(self)
        algo.traceframe = self.traceFrame
        self.queue = queue
        self.buttonFrame = ButtonFrame(self, self.queue, self.algo, self.traceFrame, self.motFrame)

        self.algo.traceframe = self.traceFrame
        self.grilleFrame = None
        self.grille = None
        self.buttonFrame.grid(row=0, column=0, sticky=N+E+S+W)
        #self.grilleFrame.grid(row=1, column=0, sticky=N+E+S+W)


    def open_grille(self, grille):
        self.grille = self.algo.grille
        print self.grille
        self.grilleFrame = GrilleFrame(self, self.grille)
        liste_mots = self.set_Grille()
        self.motFrame.listes = liste_mots
        self.motFrame.set_Mots()
        self.grilleFrame.grid(row=1, column=0, sticky=N+E+S+W)
        self.buttonFrame.grille = self.grille
        self.traceFrame.add_To_Trace("Ouverture Grille " + self.grille.nomGrille + "\n", 'curr')
        self.setDico()

    def setDico(self):
        if  self.grille:
            self.traceFrame.add_To_Trace("Ouverture Dictionnaire " + self.grille.nomDico+ "\n", 'curr')

    def setAlgo(self, algo):
        self.algo.algo = algo
        self.buttonFrame.algo.algo = algo
        self.buttonFrame.continueButton.configure(state="disabled")
        self.traceFrame.add_To_Trace("Choix de l'algorithm : " + self.algo.algo+ "\n", 'curr')



    def set_Grille(self):

        self.grille2 = [
            [None for i in range(self.grille.taille[1])]
                for j in range(self.grille.taille[0])]


        self.motVert = [GMot(self.grille.mots_verticaux[mot], self.grilleFrame, self.motFrame.frame)
                        for mot in range(len(self.grille.mots_verticaux))]
        self.motHori = [GMot(self.grille.mots_horizontaux[mot], self.grilleFrame, self.motFrame.frame)
                        for mot in range(len(self.grille.mots_horizontaux))]

        for mot in self.motVert:
            for i in range(mot.taille):
                self.grille2[mot.xStart+i][mot.yStart] = mot.caseGrilleFrame[i]

        for mot in self.motHori:
            for i in range(mot.taille):
                self.grille2[mot.xStart][mot.yStart+i] = mot.caseGrilleFrame[i]

        for mot in self.motVert:
            for mot2 in self.motHori:
                c1, c2 = mot.mot.get_Contrainte(mot2.mot)
                if c1 and c2:
                    mot.caseGrilleFrame[c1[1]].add_ui(mot2.caseGrilleFrame[c2[1]].guis)
                    mot2.caseGrilleFrame[c2[1]].add_ui(mot.caseGrilleFrame[c1[1]].guis)
                    mot.caseGrilleFrame[c1[1]] = mot2.caseGrilleFrame[c2[1]]

        font = tkFont.Font(family="Helvetica", size=7)
        for i in range(len(self.grille2)):
            for j in range(len(self.grille2[i])):
                if not self.grille2[i][j]:
                    self.grille2[i][j] = Case(self.grilleFrame, validate="key", state=DISABLED,
                                disabledbackground='black', width=5, font=font)
        for line in range(len(self.grille2)):
            for case in range(len(self.grille2[line])):
                self.grille2[line][case].grid(row=line, column=case, ipady=10)

        for mot in self.motVert:
            mot.update(None)

        for mot in self.motHori:
            mot.update(None)

        # TODO : afficher les mots sur la droite
        #self.motFrame.set_Mots([self.motVert, self.motHori])
        return [self.motHori, self.motVert]

    def updateGrille(self):
        for m in self.motHori:
            m.update(None)
        for m in self.motVert:
            m.update(None)


    def toggle_Mot(self, bool):
        if bool:
            self.motFrame.ff.grid(row=1, column=1, sticky=N+E+S+W)
        else:
            self.motFrame.ff.grid_forget()


    def toggle_Trace(self, bool):
        if bool:
            self.traceFrame.grid(row=2, column=0, columnspan=2, sticky=N+E+S+W)
        else:
            self.traceFrame.grid_forget()
