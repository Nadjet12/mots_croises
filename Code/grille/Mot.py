# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:54:07 2016

@author: Renaud ADEQUIN & Nadjet BOURDACHE
"""
from Dictionnaire import Dico


class Mot:

    ID = 1

    def __init__(self, lettres, coord, dir):
        self.id = Mot.ID
        Mot.ID += 1
        self.dir = dir
        self.value = 0
        self.lettres = lettres
        self.taille = len(lettres)
        self.xStart = coord[0]
        self.yStart = coord[1]
        self.domaineListe = []
        self.domaineValueListe = []
        self.domaine2 = None
        self.contrainteListe = []

    def str(self):
        return ""

    def setDomaine(self, copie):
        self.domaine2 = copie.copyDico()
        self.domaineListe = list(self.domaine2.get_Domaine(self.taille))
        self.domaineValueListe = list(self.domaine2.get_Domaine(self.taille, getValue=True))

    def getDomaine(self):
        return self.domaineListe
    def getValueDomaine(self):
        return self.domaineValueListe

    def ajoute_contrainte(self, obj, i):
        self.contrainteListe += [(obj, i)]

    def set_lettre(self, i, c, master):
        s = list(self.lettres)
        s[i] = c
        self.lettres = "".join(s)
        for c1, c2 in self.contrainteListe:
            if c2 is i and not self is master:
                c1.set_lettre(c2, c, master)
        
    def __repr__(self):
        dom = self.getDomaine()
        return self.dir + " id:" + str(self.id) + " " + self.lettres + " val:" + str(self.value) + " tailleDomaine:" + str(len(dom))

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
        self.domaineValueListe = list(self.domaine2.get_Domaine(self.taille, getValue=True))

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
        self.domaineValueListe = list(self.domaine2.get_Domaine(self.taille, getValue=True))
        do= self.getValueDomaine()
        if len(do) == 1:
            for d in do:
                self.lettres = d[0]
                self.value =  d[1]
        return bool

    def removeMotFromDomaine(self, mot):
        self.domaine2.removeMot(mot)
        self.domaineListe = list(self.domaine2.get_Domaine(self.taille))
        self.domaineValueListe = list(self.domaine2.get_Domaine(self.taille, getValue=True))
        do= self.getValueDomaine()
        if len(do) == 1:
            for d in do:
                self.lettres = d[0]
                self.value =  d[1]
        return


    def updateResultat(self):
        do= self.getValueDomaine()
        if len(do) == 1:
            for d in do:
                self.lettres = d[0]
                self.value =  d[1]