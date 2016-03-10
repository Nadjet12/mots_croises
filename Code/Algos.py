# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 12:16:39 2016

@author: Nadjet BOURDACHE
"""

from Grille import Grille
import Mot


def ac3(grille):
    """
    L ← {(xi, xj), i 6= j liées par une contrainte}
    tant que L 6= ∅
        choisir et supprimer dans L un couple (xi, xj)
        si revise(xi, xj) alors
            L ← L ∪ {(xk , xi) / ∃ contrainte liant xk et xi}
        fsi
    ftq
    """
    
    contrainte_Liste = grille.getContraintes()
    file_L = contrainte_Liste[::]
    while file_L is not []:
        (x,y) = file_L[0] 
        file_L = file_L[1:]
        if revise(x,y):
            if x.domaine is set():
                return False
            for (i,j) in contrainte_Liste:
                if j == x:
                    file_L += [(i,j)]
    return True
        
   

def revise(x,y):
    """
    modification ← false
    faire pour chaque v ∈ Di
        si il n'existe pas de v∈ Dj | {xi → v, xj → v} est consistante alors
            faire Di ← Di \ {v}
                modification ← vrai
            fait
    fait
    retourner modification
    """    
    modif = False
    for mot in x.domaine:
        consistant = False
        for mot2 in y.domaine:
            if consistance((x,mot),(y,mot2)):
                consistant = True
                break
        if not consistant:
            x.remove(mot)
            modif = True
    return modif
            
                    
        
def consistance((x, mot), (y, mot2)):

    if mot is mot2:
        return False

    crossPosX = [cont[1] for cont in x.contrainteListe if cont[0] is y]
    for pos in crossPosX:
        if pos == -1:
            crossPosX.remove(pos)
    if crossPosX is []:
        return True

    elif len(crossPosX) > 1:
        return False

    crossPosY = [cont[1] for cont in y.contrainteListe if cont[0] is x]
    for pos in crossPosY:
        if pos == -1:
            crossPosY.remove(pos)
    if crossPosY is []:
        return True

    if len(crossPosY) > 1:
        return False
        
    return mot[crossPosX] is mot2[crossPosY]
    
    
    
    
    