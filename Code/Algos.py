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
    while file_L:
        (x,y) = file_L[0] 
        file_L = file_L[1:]
        if revise(x,y):
            if not x.domaine :
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
    tmp = set()
    for mot in x.domaine:
        consistant = False
        for mot2 in y.domaine:
            if consistance((x,mot),(y,mot2)):
                consistant = True
                break
        if not consistant:
            print 'mot :' + str(mot) + " supprimer du domaine de " + str(x)+ " a cause de " + str(y)
            tmp.add(mot)
            modif = True

    x.remove(tmp)
    return modif
            
                    
        
def consistance((x, mot), (y, mot2)):
    # probleme consistance egalité ex: 1 (OBSADA TANTAL ZAMACH) 2 (OBSADA TANTAL ZAMACH)
    if mot == mot2:
        #print str(x)+" "+str(mot) + " egal " + str(mot2)
        #return True
        #pass
        return False

    crossPosX = [cont[1] for cont in x.contrainteListe if cont[0] is y]

    if(len(crossPosX) > 0):
        crossPosX = [item for item in crossPosX if item != -1]
    if not crossPosX:
        return True

    elif len(crossPosX) > 1:
        return False

    crossPosY = [cont[1] for cont in y.contrainteListe if cont[0] is x]

    if(len(crossPosY) > 0):
        crossPosY = [item for item in crossPosY if item != -1]
    print crossPosY
    if not crossPosY:
        return True

    if len(crossPosY) > 1:
        return False

    #print str(x)+" "+str(mot) + " end " + str(mot2) + " " + str(y) + " " + str(mot[crossPosX[0]] is mot2[crossPosY[0]])
    return mot[crossPosX[0]] is mot2[crossPosY[0]]
    
    
    
    
    