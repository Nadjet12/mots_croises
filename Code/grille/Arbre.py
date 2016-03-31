# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:22:49 2016

@author: 3501796
"""

import random
import Algos

class Noeud:

    def __init__(self, pere, motListe, motObj, couple, prof=1):
        self.pere = pere
        self.fils = []
        self.listeMot = motListe
        self.motObj = motObj
        self.mot = couple[0]
        if self.pere:
            self.value = min(couple[1], self.pere.value)
            self.listeMotsAttribue = self.pere.listeMotsAttribue + [(motObj, couple[0])]
        else:
            self.value = couple[1]
            self.listeMotsAttribue = [(motObj, couple[0])]
        self.prof = prof

    def getValue(self):
        return self.value
        
    def create_Fils(self, algo):
        if not self.listeMot:
            # si la liste est vide ce noeud est la meilleur solution            
            return self
            
        m = self.listeMot[0]

        for mot in m.getValueDomaine():
            if not mot in [self.listeMotsAttribue[i][0] for i in range(len(self.listeMotsAttribue))]:
                consist = True
                for motAtt in self.listeMotsAttribue:
                    if not algo.consistance((motAtt[0], motAtt[1]), (m, mot) ):
                        break
                if consist:
                    self.fils += [Noeud(self, self.listeMot[1:], m, mot, self.prof+1)]
        return self.fils
        

class Arbre:
    
    def __init__(self, motListe, algo):
        self.listeNoeud = []
        self.solution = None
        mot = motListe.pop(0)
        for el in mot.getValueDomaine():
            self.listeNoeud += [Noeud(None, motListe, mot, el)]
        self.algo = algo
        #sorted(self.listeNoeud, key=lambda value: (value[1]), reverse=True)


    def get_Noeud_Max(self):
        """ sans sort """
        # supprimer le noeud max de la liste
        #liste = [self.listeNoeud[i].value for i in range(len(self.listeNoeud))]
        #valMax =  max(liste)
        #min(LL, key=lambda item:item[1])
        #posMax = [i for i in range(len(liste)) if self.listeNoeud[i].value == valMax]

        # si la liste contient plusieur élément max on en prend un aléatoirement
        # Choisir le noeud le plus profond
        #pos = random.choice(posMax)

        # Si plusieur Noeud son max peut-être utiliser une heuristique
        return self.listeNoeud.pop(0)



    def update(self):
        # prend le noeud max et developpe ses fils a la liste des Noeuds

        n = self.get_Noeud_Max()

        l = n.create_Fils(self.algo)
        if isinstance(l, Noeud):
            # si l est un Noeud alors c'est la solution optimal
            self.solution = l
            return l
        else:
            # sinon c'est une liste de Noeud
            self.listeNoeud += l

            #sorted(self.listeNoeud, key=lambda value: (value[1]), reverse=True)