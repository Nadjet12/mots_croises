# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:22:49 2016

@author: 3501796
"""

import random
import Algos
from FastTable import FastTable
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
        self.fils = FastTable()
        self.listeMot = motListe[:]
        self.motObj = motObj
        self.mot = couple[0]
        if self.pere:
            self.value = min(couple[1], self.pere.value)
            self.listeMotsAttribue = self.pere.listeMotsAttribue + [(self.motObj, self.mot)]
        else:
            self.value = couple[1]
            self.listeMotsAttribue = [(self.motObj, self.mot)]
        self.prof = prof

    def getValue(self):
        return self.value


    def create_Fils(self, algo, liste ):
        #print len(self.listeMot)
        if not self.listeMot:
            # si la liste est vide ce noeud est la meilleur solution            
            return self

        xk = algo.heur(self.listeMot, None)
        self.listeMot.remove(xk)
        for mot in xk.getValueDomaine():
            if len(algo.consistante(self.listeMotsAttribue, (xk, mot[0]))) == 0:
                n = Noeud(self, self.listeMot[:], xk, mot, self.prof+1)
                t = (n.value, n)
                liste.insert(t)
        

class Arbre:
    NBUPDATE = 0
    def __init__(self, motListe, algo):
        self.listeNoeud = FastTable()
        self.solution = None
        mot = algo.heur(motListe, None)
        motListe.remove(mot)
        for el in mot.getValueDomaine():
            t = (el[1], Noeud(None, motListe, mot, el))
            self.listeNoeud.insert(t)


        self.algo = algo


    def get_Noeud_Max(self):
        maxtuple = self.listeNoeud.tail()
        maxval = maxtuple[0]
        if len(self.listeNoeud) == 0:
            return maxtuple[1]
        tmp = self.listeNoeud.tail()

        tableMax = [maxtuple]

        while tmp[0] == maxval and len(self.listeNoeud)>0:
            tableMax += [tmp]
            tmp = self.listeNoeud.tail()
        self.listeNoeud.insert(tmp)

        elmax = max(tableMax,key=lambda x:x[1].prof)
        tableMax.remove(elmax)
        for el in tableMax:
            self.listeNoeud.insert(el)
        print str(elmax[0]) + " " + str(elmax[1].mot) + "  " + str(elmax[1].prof) + "   "+ str(elmax[1].motObj)
        return elmax

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
        Arbre.NBUPDATE += 1
        #print 'appel a update = ' + str(Arbre.NBUPDATE)

        # prend le noeud max et developpe ses fils a la liste des Noeuds
        n = self.get_Noeud_Max()

        l = n[1].create_Fils(self.algo, self.listeNoeud)
        if isinstance(l, Noeud):
            # si l est un Noeud alors c'est la solution optimal
            self.solution = l
            #print 'hello'
            return l
        '''
        else:
            # sinon c'est une liste de Noeud
            #for node in l:
                #pos = self.getPosInsertion(self.listeNoeud, node.value, 0, len(self.listeNoeud)-1)
                #self.listeNoeud.insert(pos, node)
            while len(l) != 0:
                el = l.tail()
                self.listeNoeud.insert(el)
            #print (len(self.listeNoeud))
        '''


