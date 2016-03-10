# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 16:54:07 2016

@author: Nadjet BOURDACHE
"""

class Mot:
    
    def __init__(self, lettres, coord):
        self.lettres = lettres
        self.taille = len(lettres)
        self.xStart = coord[0]
        self.yStart = coord[1]
        self.domaine = set()
        self.contrainteListe = []
        
        
    def ajoute_contrainte(self, obj, i):
        self.contrainteListe += [(obj, i)]

    def remove(self, mot):
        self.domaine.remove(mot)
        
    def __repr__(self):
        return self.lettres + str(type(self.lettres))