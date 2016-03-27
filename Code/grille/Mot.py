# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:54:07 2016

@author: Nadjet BOURDACHE
"""
from grille.Dictionnaire import Dico


class Mot:

    ID = 1

    def __init__(self, lettres, coord, dir):
        self.id = Mot.ID
        Mot.ID = Mot.ID + 1
        self.dir = dir
        self.value = 0
        self.lettres = lettres
        self.taille = len(lettres)
        self.xStart = coord[0]
        self.yStart = coord[1]
        self.domaineListe = []
        self.domaine2 = None
        self.contrainteListe = []

    def setDomaine(self, copie):
        self.domaine2 = copie.copyDico()
        self.domaineListe = list(self.domaine2.get_Domaine(self.taille))

    def getDomaine(self):
        return self.domaineListe

    def ajoute_contrainte(self, obj, i):
        self.contrainteListe += [(obj, i)]

    def set_lettre(self, i, c):
        s = list(self.lettres)
        # print str(i) + " " + c
        s[i] = c
        self.lettres = "".join(s)
        for c1, c2 in self.contrainteListe:
            if c2 is i:
                c1.update(self, c)

    def update(self, mot, c):
        for c1,c2 in self.contrainteListe:
            if c1 is mot:
                s = list(self.lettres)
                s[c2] = c
                self.lettres = "".join(s)

        
    def __repr__(self):
        dom = self.getDomaine()
        return self.dir + " id=" + str(self.id) + " Position=(" +str(self.xStart) + "," + \
               str(self.yStart) + ") :" + self.lettres + ": \t\t\tTaille du mot " + \
               str(self.taille) + " tailleDomaine:" + str(len(dom))

    def get_Contrainte(self, mot):
        c1 = None
        c2 = None

        for c in self.contrainteListe:
            if c[0] is mot and not c[1] is -1:
                c1 = c
        if not c1:
            return c1, c2

        for c in mot.contrainteListe:
            if c[0] is self and not c[1] is -1:
                c2 = c

        return c1, c2

    def initDomaine(self, liste):

        self.domaine2 = Dico(liste=liste)
        self.domaineListe = list(self.domaine2.get_Domaine(self.taille))

    def printDomaineSize(self):
        print str(self) + " -> " + str(len(self.domaine2.get_Domaine(self.taille)))

    def getContraintsX(self, x):
        return [cont[1] for cont in self.contrainteListe if cont[0] is x]

    def getContraintsXE(self, x):
        c = [cont[1] for cont in self.contrainteListe if cont[0] is x]

        c = [item for item in c if item != -1]
        return c[0]

    def getAllLettre(self, indiceY):
        if self.lettres[indiceY] is ' ':
            return self.domaine2.getAllLettre(indiceY)
        return self.lettres[indiceY]

    def updateFromContraintes(self, contrainte, yLettre):
        bool = self.domaine2.updateFromContraintes(contrainte, yLettre)
        self.domaineListe = list(self.domaine2.get_Domaine(self.taille))
        do= self.getDomaine()
        if len(do) == 1:
            for d in do:
                self.lettres = d
        return bool

    def removeMotFromDomaine(self, mot):
        self.domaine2.removeMot(mot)
        self.domaineListe = list(self.domaine2.get_Domaine(self.taille))
        do= self.getDomaine()
        if len(do) == 1:
            for d in do:
                self.lettres = d
        return


    def updateResultat(self):
        do= self.getDomaine()
        if len(do) == 1:
            for d in do:
                self.lettres = d