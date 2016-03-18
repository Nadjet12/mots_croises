# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:54:07 2016

@author: Nadjet BOURDACHE
"""
from grille.Dictionnaire import Dico


class Mot:

    ID = 1

    def __init__(self, lettres, coord):
        self.id = Mot.ID
        Mot.ID = Mot.ID + 1
        self.lettres = lettres
        self.taille = len(lettres)
        self.xStart = coord[0]
        self.yStart = coord[1]
        #self.domaine = set()
        self.domaine2 = None
        self.contrainteListe = []
        
    def getDomaine(self):
        return list(self.domaine2.get_Domaine(self.taille))

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


    def remove(self, mot):
        for m in mot:
            self.domaine.remove(m)
        if len(self.domaine) == 1:
            for d in self.domaine:
                self.lettres = d
        
    def __repr__(self):
        return "id : " + str(self.id) + " " +str(self.xStart) + "," + str(self.yStart) + ":" + self.lettres + ":" + str(self.taille) + "-> " + str(self.getDomaine())

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

    #def initDomaine(self, dico):
    #    m = self.lettres.replace(' ', '.')
    #    d = dico.get_New_Domaine(m)
    #    for i in d:
    #        self.domaine.add(str(i.encode('utf-8')))

    def initDomaine(self, liste):

        self.domaine2 = Dico(liste=liste)

    def get_Domaine(self):
        return self.domaine2.get_Domaine(self.taille)

    def printDomaine(self):
        #s = ""
        #for m in self.domaine2:
        #    s += str(m)+" "
        print str(self)

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
        do= self.get_Domaine()
        if len(do) == 1:
            for d in do:
                self.lettres = d
        return self.domaine2.updateFromContraintes(contrainte, yLettre)

    def updateResultat(self):
        do= self.get_Domaine()
        if len(do) == 1:
            print self
            for d in do:
                self.lettres = d