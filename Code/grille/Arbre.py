# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:22:49 2016

@author: 3501796
"""

import random

class Noeud:

    def __init__(self, pere, motListe, motObj, couple):
        self.pere = pere
        self.fils = []
        self.listeMot = motListe
        self.motObj = motObj
        self.mot = couple[0]
        self.value = couple[1]

        
        
    def create_Fils(self):
        if not self.listeMot:
            # si la liste est vide ce noeud est la meilleur solution            
            return self
            
        m = self.listeMot[0]
        for mot in m.getDomaine():
            self.fils += [Noeud(self, self.listeMot[1:], m, mot)]

        return self.fils
        

class Arbre:
    
    def __init__(self, motListe):
        self.listeNoeud = []
        self.solution = None
        mot = motListe.pop(0)
        for el in mot.getDomaine():
            self.listeNoeud += [Noeud(None, motListe, mot, el)]
        sorted(self.listeNoeud, key=lambda value: (value[1]), reverse=True)
<<<<<<< HEAD
    
=======
        
>>>>>>> origin/master

    def get_Noeud_Max(self):
        """ sans sort """
        # supprimer le noeud max de la liste
        liste = [self.listeNoeud[i].value for i in range(len(listeNoeud))]
        valMax =  max(liste)
        posMax = [i for i in range(len(liste)) if self.listeNoeud[i].value == valMax]

        # si la liste contient plusieur élément max on en prend un aléatoirement
        pos = random.choice(posMax)

        # Si plusieur Noeud son max peut-être utiliser une heuristique
        return self.listeNoeud.pop(pos)
        """
        avec sort ça donnerait

        elemMax = self.listeNoeud[0]
        pos = 1
        while pos < len(self.listeNoeud) and self.listeNoeud[pos] == elemMax
            pos++
        liste = self.listeNoeud[:pos]
        pos = random.choice(liste)
        return self.listeNoeud.pop(pos)  """


    def update(self):
        # prend le noeud max et developpe ses fils a la liste des Noeuds

        n = self.get_Noeud_Max
        l = n.create_Fils()
        if isinstance(l, Noeud):
            # si l est un Noeud alors c'est la solution optimal
            self.solution = l
            return l
        else:
            # sinon c'est une liste de Noeud
            self.listeNoeud += l
            sorted(self.listeNoeud, key=lambda value: (value[1]), reverse=True)