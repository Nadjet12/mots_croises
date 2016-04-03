# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12.mc:22:49 2016

@author: Renaud ADEQUIN & Nadjet BOURDACHE
"""

import Algos
from FastTable import FastTable

NBMANMAX = 0

class Noeud:

    def __init__(self, pere, motListe, motObj, couple, prof=1):
        self.pere = pere
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


    def __repr__(self):
        return "id:" +str(self.motObj.id) + " "+self.mot + " value:" +str(self.value) + ": prof " + str(self.prof)

    def getValue(self):
        return self.value


    def create_Fils(self, algo, liste ):

        if not self.listeMot:
            # Si la liste des mots a instancier est vide, le noeud fils est la meilleure solution
            return self

        # Sinon on crée une liste de fils
        # Mais uniquement les valeurs de mots coérrantes avec le reste de variables déja instanciées
        xk = algo.heuristique_instance_max(self.listeMot, self.listeMotsAttribue)
        self.listeMot.remove(xk)
        for mot in xk.getValueDomaine():
            if len(algo.consistante(self.listeMotsAttribue, (xk, mot[0]))) == 0:
                n = Noeud(self, self.listeMot[:], xk, mot, self.prof+1)
                t = (n.value, n)
                liste.insert(t)


class Arbre:
    def __init__(self, motListe, algo):
        self.listeNoeud = FastTable()
        self.solution = None
        mot = algo.heur(motListe, None)
        motListe.remove(mot)
        for el in mot.getValueDomaine():
            t = (el[1], Noeud(None, motListe[:], mot, el))
            self.listeNoeud.insert(t)

        self.algo = algo

    # Fonction qui retourne la feuille possédant la valeur maximum
    # En cas d'égalité, on prend le noeuds le plus profond
    def get_Noeud_Max(self):
        global NBMANMAX
        maxtuple = self.listeNoeud.tail()
        maxval = maxtuple[0]

        # S'il ne reste plus qu'une varible à instanncier on la retourne
        if len(self.listeNoeud) == 0:
            return maxtuple

        # Sinon on récupère tout les noeuds de la liste qui ont la valeur max
        tmp = self.listeNoeud.tail()
        tableMax = [maxtuple]

        while tmp[0] == maxval and len(self.listeNoeud)>0:
            tableMax += [tmp]
            tmp = self.listeNoeud.tail()
        self.listeNoeud.insert(tmp)

        # Parmi les noeuds récupérés, on récupère le plus profond
        elmax = max(tableMax,key=lambda x:x[1].prof)
        tableMax.remove(elmax)
        # On remet les autres noeuds dans la liste
        for el in tableMax:
            self.listeNoeud.insert(el)
        # On renvoi le noeud choisi
        return elmax

    # Fonction de mise à jour de l'arbre
    def update(self):
        # Récupère le noeud max parmis les feuilles et crée ses fils puis les ajoutes à la liste de feuilles
        if len(self.listeNoeud) > 0:
            n = self.get_Noeud_Max()
        else:
            return "Pas de solution"

        l = n[1].create_Fils(self.algo, self.listeNoeud)
        if isinstance(l, Noeud):
            # Si l est un Noeud et non une liste alors c'est la solution optimale
            self.solution = l
            return l


