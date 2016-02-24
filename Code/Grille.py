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
    
    def __init__(self, filePath=None, taille=(20,10), dictionnaire="./mots/135000-mots-fr.txt", alea = False):
       
        self.mots_verticaux = []
        self.mots_horizontaux = []
        self.cases_noires = []
        self.taille = taille
        self.dico = Dico(dictionnaire)
        
        if alea == True:
            filePath = self.genereGrilleAlea(taille)
            
        self.detecte_mots(filePath)
        
#        print self.mots_horizontaux
#        print self.mots_verticaux
        
#    def readFromFile(self, filePath=None):  
#        fichier = open(filePath, encoding="ISO-8859-1")
#        self.taille = eval(fichier.readline())
#        mot = fichier.readline()   
#        while mot not in '\r\n':
#            mot = mot.split(" ")    
##            print(mot)
#            self.mots_horizontaux += [Mot(str(mot[0]), eval(mot[1]))]
#            mot = fichier.readline()
#        
#        while mot not in '\r\n':
#            mot = mot.split(" ")
#            self.mots_verticaux += [Mot(str(mot[0]), eval(mot[1]))]
#            mot = fichier.readline()
#        fichier.close
        
    def detecte_mots(self, filePath):
        
        fichier = open(filePath, "r")
        taille = eval(fichier.readline())
        self.taille = taille
        tab = [[True for i in range(taille[1])] for j in range(taille[0])]
        
        for i in range(taille[0]):
            ligne = fichier.readline()
            for j in range(taille[1]):
                if ligne[j] == "$":                
                    tab[i][j] = False
                
        for i in range(len(tab)):
            start = [i,0]            
            mot = False
            taille = 0
            for j in range(len(tab[i])):
                if tab[i][j] and not mot:
                    mot = True
                    start[1] = j
                elif not tab[i][j] and mot:
                    mot = False
                    taille = j-start[1]
                    if taille > 1 :
                        self.mots_horizontaux += [Mot(''.join(['.' for k in range(taille)]), start)]
                    
        for j in range(len(tab)):
            start = [0,j]         
            mot = False
            taille = 0
            for i in range(len(tab[i])):
                if tab[i][j] and not mot:
                    mot = True
                    start[1] = i
                elif not tab[i][j] and mot:
                    mot = False
                    taille = i-start[1]
                    if taille > 1 :
                        self.mots_verticaux += [Mot(''.join(['.' for k in range(taille)]), start)]
                    
        
    def genereGrilleAlea(self, taille):
        self.taille = taille
        nbNoires = (float(random.randrange(20,30))/100) * float(taille[0]) * float(taille[1])
        nbNoires = int(nbNoires)
        while nbNoires > 0:
            x = random.randrange(taille[0])
            y = random.randrange(taille[1])
            if (x,y) not in self.cases_noires:
                self.cases_noires += [(x,y)]
                nbNoires -= 1
        self.fichierSortie()
                
                
    def fichierSortie(self):
        path = "./grillesVides/doc.txt"
        fichier = open(path, "w")
        fichier.write(str(self.taille) + "\n")
        for i in range(self.taille[0]):
            for j in range(self.taille[1]):
                if (i,j) in self.cases_noires:
                    fichier.write("$")
                else:
                    fichier.write(".")
            fichier.write("\n")
        fichier.close
        return path
        
        
            
t = (20,20)
g = Grille("./grillesVides/doc.txt",True)

# 
g = Grille("./doc.txt")
print(g.taille)
print(type(g.taille[0]))