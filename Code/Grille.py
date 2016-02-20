# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 13:06:47 2016

@author: Nadjet BOURDACHE
"""

from codecs import *
from Dictionnaire import Dico
from Mot import Mot
import random

class Grille:
    
    def __init__(self, filePath=None, taille=(10,10), dictionnaire="./mots/135000-mots-fr.txt"):
        self.mots_verticaux = []
        self.mots_horizontaux = []
        self.dico = None
        self.cases_noires = []
        fichier = open(filePath, encoding="ISO-8859-1")
        
        self.taille = eval(fichier.readline())
        
        mot = fichier.readline()        
        
        while mot not in '\r\n':
            mot = mot.split(" ")    
            print(mot)
            self.mots_horizontaux += [Mot(str(mot[0]), eval(mot[1]))]
            mot = fichier.readline()
        
        while mot not in '\r\n':
            mot = mot.split(" ")
            self.mots_verticaux += [Mot(str(mot[0]), eval(mot[1]))]
            mot = fichier.readline()
        
        self.dico = Dico(dictionnaire)
        
        print self.mots_horizontaux
        print self.mots_verticaux
        
    def detecte_mots(self, tab):
        for i in range(len(tab)):
            start = (i,0)            
            mot = False
            taille = 0
            for j in range(len(tab[i])):
                if tab[i,j] and not mot:
                    mot = True
                    start[1] = j
                elif not tab[i][j] and mot:
                    mot = False
                    taille = j-start[1]
                    self.mots_horizontaux += [Mot(''.join(['.' for k in range(taille)]), start)]
                    
        
    def genereGrille(taille):
        proba = random(20,30)/100
        
        
        
# 
#g = Grille("./doc.txt")
#print(g.taille)
#print(type(g.taille[0]))