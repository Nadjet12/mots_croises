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
    
    def __init__(self, filePath=None, taille=(20,10), dictionnaire="./mots/135000-mots-fr.txt", alea=False):
       
        self.mots_verticaux = []
        self.mots_horizontaux = []
        self.cases_noires = []
        self.taille = taille
        self.dico = Dico(dictionnaire)
        
        if alea:
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
        
        for i in range(taille[0]):
            ligne = fichier.readline()
            tab[i] = [j for j in ligne]             
                
        for i in range(len(tab)):
            start = [i,0]
            mot = ""
            for j in range(len(tab[0])):
                if tab[i][j] != "$":
                    if len(mot) == 0:
                        start[1] = j
                    mot += tab[i][j]
                elif tab[i][j] == "$" and len(mot) > 1:
                    self.mots_horizontaux += [Mot(''.join([k for k in mot]), start)]
                    
        for j in range(len(tab[0])):
            start = [0,j]
            mot = ""
            for i in range(len(tab)):
                if tab[i][j] != "$":
                    if len(mot) == 0:
                        start[1] = i
                    mot += tab[i][j]
                elif tab[i][j] == "$" and len(mot) > 1:
                    self.mots_verticaux += [Mot(''.join([k for k in mot]), start)]
        
                    
        
    def genereGrilleAlea(self, taille):
        self.taille = taille
        nbNoires = (float(random.randrange(20,30))/100) * float(taille[0]) * float(taille[1])
        nbNoires = int(nbNoires)
        blackList = []
        while nbNoires > 0:
            x = random.randrange(taille[0])
            y = random.randrange(taille[1])
            if (x,y) not in self.cases_noires and (x,y) not in blackList:
                blackList += [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]
                self.cases_noires += [(x,y)]
                nbNoires -= 1
        return self.fichierSortie()
                
                
    def fichierSortie(self):
        path = "./grillesVides/sortie.txt"
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
        
    def getContraintes(self):
        liste = []
        for m in self.mots_verticaux:
            for mot2 in m.egalContrainteListe:
                liste += [(m,mot2[0])]
        
        for m in self.mots_horizontaux:
            for mot2 in m.egalContrainteListe:
                liste += [(m,mot2[0])]
        return liste
            
t = (20,20)
g = Grille(taille=t,alea=True)

# 
#g = Grille("./doc.txt")
print(g.taille)
print(type(g.taille[0]))