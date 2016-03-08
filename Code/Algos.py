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
    
    contrainte_Liste = []
    file_L = contrainte_Liste[::]
    # remplir la liste des contraintes     
    while file_L is not []:
        (x,y) = file_L[0] 
        file_L = file_L[1:]
        if revise(x,y):
            for (i,j) in contrainte_Liste:
                if j == x:
                    file_L += [(i,j)]
        
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
# a un moment il faut vérifier que le domaine n'est pas vide

def revise(x,y):
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
    #crossPosX = []
    #crossPosX = [x.egalContrainteListe[i][1] for i in range(x.egalContrainteListe) if x.egalContrainteListe[i][0] == mot2]
    # il faut tester les objets et pas les srings (je crois) :-)
    crossPosX = [cont[1] for cont in x.egalContrainteListe if cont[0] is y]
    if crossPosX is []:
        return True
    elif len(crossPosX) > 1:
        # 2 mots ne peuvent pas se croiser plusieurs fois :-) => erreur implémentation
        return False
    crossPosX = crossPosX[0]
    #crossPosY = [y.egalContrainteListe[i][1] for i in range(y.egalContrainteListe) if y.egalContrainteListe[i][0] == mot]
    crossPosY = [cont[1] for cont in y.egalContrainteListe if cont[0] is x]
    if len(crossPosY) > 1:
        return False
    crossPosY = crossPosY[0]
    '''
    if mot[crossPosX] != mot2[crossPosY]:
        return False
    return True
    '''
    return mot[crossPosX] is mot2[crossPosY]
    
    
    
    
    