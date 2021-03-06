# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 13:06:47 2016

@author: Renaud ADEQUIN & Nadjet BOURDACHE
"""

from codecs import *
from Mot import Mot
import random
import numpy

GRILLE_PATH = '../Data/grillesVides/'


class Grille:
    def __init__(self, filePath=None, taille=(20, 10), alea=False, percent=None):
        Mot.ID = 1
        self.mots_verticaux = []
        self.mots_horizontaux = []
        self.cases_noires = []
        self.taille = taille
        self.dico = None
        self.filePath = filePath
        if alea:
            self.filePath = self.genereGrilleAlea(taille, percent)
            self.nomGrille = "Random "+str(taille)
        else:
            self.nomGrille = self.filePath.split("/")[-1]

        self.detecte_mots(self.filePath)
        self.defContraintes()


    def get_Domaines_Sizes(self):
        s = 0
        for m in self.mots_horizontaux + self.mots_verticaux:
            s += len(m.getDomaine())
        return s

    # Détecte les mots et leurs emplacements à partir d'un fichier
    def detecte_mots(self, filePath):

        fichier = open(filePath, "r")
        taille = eval(fichier.readline())
        self.taille = taille
        tab = numpy.ones((taille[0], taille[1]), str)

        for i in range(taille[0]):
            ligne = fichier.readline()
            tab[i] = [j for j in ligne[:-1]]

        for i in range(len(tab)):
            start = [i, 0]
            mot = ""
            for j in range(len(tab[0])):
                if tab[i][j] != "$":
                    if len(mot) == 0:
                        start[1] = j
                    mot += tab[i][j]
                    if j == (len(tab[0]) - 1) and len(mot) > 1:
                        self.mots_horizontaux += [Mot(''.join([k for k in mot]), start, "Horizontal")]
                elif tab[i][j] == "$":
                    self.cases_noires += [(i, j)]
                    if len(mot) > 1:
                        self.mots_horizontaux += [Mot(''.join([k for k in mot]), start, "Horizontal")]
                    if len(mot) > 0:
                        mot = ""

        for j in range(len(tab[0])):
            start = [0, j]
            mot = ""
            for i in range(len(tab)):
                if tab[i][j] != "$":
                    if len(mot) == 0:
                        start[0] = i
                    mot += tab[i][j]
                    if i == (len(tab) - 1) and len(mot) > 1:
                        self.mots_verticaux += [Mot(''.join([k for k in mot]), start, "Vertical")]
                elif tab[i][j] == "$" or i == (len(tab) - 1):
                    self.cases_noires += [(i, j)]
                    if len(mot) > 1:
                        self.mots_verticaux += [Mot(''.join([k for k in mot]), start, "Vertical")]
                    if len(mot) > 0:
                        mot = ""

    # Génération d'une grille aléatoire
    def genereGrilleAlea(self, taille, percent=None):
        self.taille = taille
        if not percent:
            nbNoires = (float(random.randrange(30, 40)) / 100) * float(taille[0]) * float(taille[1])
        else:
            nbNoires = (float(percent) / 100) * float(taille[0]) * float(taille[1])
        nbNoires = int(nbNoires)
        tab = numpy.ones((taille[0], taille[1]), str)

        while nbNoires > 0:
            x = random.randrange(taille[0])
            y = random.randrange(taille[1])
            if tab[x][y] != "$":
                tab[x][y] = "$"
                nbNoires -= 1

        for i in range(taille[0]):
            sstr = ""
            for j in range(taille[1]):
                sstr += tab[i][j]
                if tab[i][j] != "$":
                    if ((i > 0 and tab[i - 1][j] == "$") and (i < taille[0] - 1 and tab[i + 1][j] == "$") and
                            (j > 0 and tab[i][j - 1] == "$") and (j < taille[1] - 1 and tab[i][j + 1] == "$")):
                        tab[i][j] = "$"
                    else:
                        tab[i][j] = " "

        return self.fichierSortie(tab)

    # Création d'un fichier texte pour sauvegarder une grille à partir d'un tableau
    def fichierSortie(self, tab):
        path = GRILLE_PATH+ "tmp.mc"
        fichier = open(path, "w")
        fichier.write(str(self.taille) + "\n")
        for i in range(self.taille[0]):
            for j in range(self.taille[1]):
                fichier.write(tab[i][j])
            fichier.write("\n")
        fichier.close()
        return path

    # Définie la liste des contraintes qu'a chaque mot avec les autres
    def defContraintes(self):
        for mot in self.mots_horizontaux:
            " mots horizontaux de même taille "
            for mot2 in self.mots_horizontaux:
                if mot != mot2 and mot.taille == mot2.taille:
                    mot.contrainteListe += [(mot2, -1)]
                    mot2.contrainteListe += [(mot, -1)]
            " mots verticaux "
            for mot2 in self.mots_verticaux:
                if mot.taille == mot2.taille:
                    mot.contrainteListe += [(mot2, -1)]
                    mot2.contrainteListe += [(mot, -1)]
                if (mot.xStart in range(mot2.xStart, mot2.taille + mot2.xStart) and
                            mot2.yStart in range(mot.yStart, mot.taille + mot.yStart)):
                    mot.ajoute_contrainte(mot2, mot2.yStart - mot.yStart)
                    mot2.ajoute_contrainte(mot, mot.xStart - mot2.xStart)

        for mot in self.mots_verticaux:
            for mot2 in self.mots_verticaux:
                if mot != mot2 and mot.taille == mot2.taille:
                    mot.contrainteListe += [(mot2, -1)]
                    mot2.contrainteListe += [(mot, -1)]


    # Retourne la liste des contraintes entre toutes les paires de noeuds de la grille
    def getContraintes(self):
        liste = []
        for m in self.mots_verticaux:
            for mot2 in m.contrainteListe:
                liste += [(m, mot2[0])]

        for m in self.mots_horizontaux:
            for mot2 in m.contrainteListe:
                liste += [(m, mot2[0])]
        return liste


    # Mise à jour d'un dictionnaire et initialisation des domaines deds mots de la grille
    def updateDico(self, dico):
        self.dico = dico
        self.initDomaine()


    # Initialisation des domaines des mots de la grille
    def initDomaine(self):
        for m in self.mots_horizontaux + self.mots_verticaux:
            h = m.lettres
            h = h.replace(' ', '.')
            m.initDomaine(self.dico.get_New_Domaine(h, getValue=True))


    # Récupère le résultat d'un algo sous forme de grille, et affecte les bonne valeur à chaque variable
    def setResultat(self, list):
        for m in list:
            m[0].lettres = m[1]
            if len(m) > 2:
                m[0].value = m[2]


    # Retourne le nombre de mots de la grille
    def motSize(self):
        return len(self.mots_horizontaux) + len(self.mots_verticaux)


    # Sauvegarde une grille dans un fichier texte à partir d'un objet grille
    def sauvegarder_grille(self, filePath):

        fichier = open(filePath, "w")
        fichier.write(str(self.taille))
        fichier.write("\n")
        tab = numpy.ones((self.taille[0], self.taille[1]), str)

        for mot in self.mots_horizontaux:
            i = mot.xStart
            j = mot.yStart
            for k in range(j,j+mot.taille):
                tab[i][k] = mot.lettres[k-j]

        for mot in self.mots_verticaux:
            i = mot.xStart
            j = mot.yStart
            for k in range(i,i+mot.taille):
                tab[k][j] = mot.lettres[k-i]

        for coord in self.cases_noires:
            tab[coord[0]][coord[1]] = "$"
        for i in range(self.taille[0]):
            fichier.write(tab[i])
            fichier.write("\n")

        fichier.close()

