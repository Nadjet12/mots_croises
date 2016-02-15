# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:54:07 2016

@author: Nadjet BOURDACHE
"""

class Mot:
    
    def __init__(self, taille, x, y):
        self.lettres = ["." for i in range(taille)]
        self.taille = taille
        self.xStart = x
        self.yStart = y
        self.domaine = set()
        self.egalContrainteListe = []
        
        
    def ajoute_contrainte(self, obj, i):
        self.egalContrainteListe += [(obj, i)]