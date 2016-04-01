# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:22:49 2016

@author: 3501796
"""

import random
import Algos
from collections import deque
import bisect

class FunkyDeque(deque):
    def _insert(self, index, value):
        self.rotate(-index)
        self.appendleft(value)
        self.rotate(index)

    def insert(self, value):
        self._insert(bisect.bisect_left(self,value), value)

    def __init__(self, iterable):
        super(FunkyDeque, self).__init__(sorted(iterable, key=lambda x: x.prof, reverse=True))


class Noeud:

    def __init__(self, pere, motListe, motObj, couple, prof=1):
        self.pere = pere
        self.fils = []
        self.listeMot = motListe[:]
        self.motObj = motObj
        self.mot = couple[0]
        if self.pere:
            self.value = min(couple[1], self.pere.value)
            self.listeMotsAttribue = self.pere.listeMotsAttribue + [(self.pere.motObj, self.pere.mot)]
        else:
            self.value = couple[1]
            self.listeMotsAttribue = []
        self.prof = prof

    def getValue(self):
        return self.value


    def create_Fils(self, algo):
        print len(self.listeMot)
        if not self.listeMot:
            # si la liste est vide ce noeud est la meilleur solution            
            return self

        xk = algo.heur(self.listeMot, None)
        self.listeMot.remove(xk)
        #m = self.listeMot[0]
        '''
        for mot in m.getValueDomaine():
            if not mot in [self.listeMotsAttribue[i][0] for i in range(len(self.listeMotsAttribue))]:
                consist = True
                for motAtt in self.listeMotsAttribue:
                    if not algo.consistance((motAtt[0], motAtt[1]), (m, mot) ):
                        consist = False
                        break
                if consist:
                    self.fils += [Noeud(self, self.listeMot[1:], m, mot, self.prof+1)]
        '''
        for mot in xk.getValueDomaine():
            if len(algo.consistante(self.listeMotsAttribue, (self.motObj, self.mot))) == 0:
                self.fils += [Noeud(self, self.listeMot[:], xk, mot, self.prof+1)]

        return self.fils
        

class Arbre:
    
    def __init__(self, motListe, algo):
        self.listeNoeud = []
        self.solution = None
        mot = motListe.pop(0)
        for el in mot.getValueDomaine():
            self.listeNoeud += [Noeud(None, motListe, mot, el)]
        self.listeNoeud = sorted(self.listeNoeud, key=lambda x: x.value, reverse=True)
        #self.listeNoeud = FunkyDeque(self.listeNoeud)
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
        #i = 0
        #while self.listeNoeud[i].value == self.listeNoeud[0].value:
         #   i += 1
        #liste = self.listeNoeud[:i]
        #elmax = max(liste,key=lambda x:x.prof)
        #self.listeNoeud.remove(elmax)
        #print "prof = " + str(elmax.prof)
        return self.listeNoeud.pop(0)

    def getPosInsertion(self, list , val, deb, fin):
        if deb < fin:
            if list[deb].value <= val:
                return deb
            if list[fin].value >= val:
                return fin+1

            milieu = int((fin+deb)/2)
            if list[milieu] == val:
                return milieu
            if list[milieu].value > val:
                return self.getPosInsertion(list, val, milieu+1, fin)
            return self.getPosInsertion(list, val, deb, milieu-1)
        return fin


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
            for node in l:
                pos = self.getPosInsertion(self.listeNoeud, node.value, 0, len(self.listeNoeud)-1)
                self.listeNoeud.insert(pos, node)
                #self.listeNoeud.insert(node)
            #print (len(self.listeNoeud))

