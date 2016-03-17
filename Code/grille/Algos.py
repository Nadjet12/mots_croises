# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 12:16:39 2016

@author: Nadjet BOURDACHE
"""
import threading
import time
import random

from grille import Grille
import Mot


class Algo(threading.Thread):
    def __init__(self, queue=None, grille=None, traceframe=None, algo=None):
        threading.Thread.__init__(self)
        self.queue = queue
        self.grille = grille
        self.traceframe = traceframe
        self.algo = algo
        self.res = None

    def run(self):
        if self.algo is "AC3":
            bool = self.ac3()
            if self.queue:
                self.queue.put(bool)
        elif self.algo is "RAC":
            bool = self.RAC([], self.grille.mots_horizontaux + self.grille.mots_verticaux)
            if self.queue:
                self.queue.put(self.res)
        else:
            print "Error"

    def ac3(self):
        """
        L ← {(xi, xj), i 6= j liées par une contrainte}
        tant que L 6= ∅
            choisir et supprimer dans L un couple (xi, xj)
            si revise(xi, xj) alors
                L ← L ∪ {(xk , xi) / ∃ contrainte liant xk et xi}
            fsi
        ftq
        """
        start_time = time.time()
        if self.traceframe:
            self.traceframe.add_To_Trace("Debut de l'AC3\n", 'in')
        contrainte_Liste = self.grille.getContraintes()
        file_L = contrainte_Liste[::]
        while file_L:
            (x, y) = file_L[0]
            file_L = file_L[1:]
            if self.revise(x, y):
                if not x.domaine:
                    return False
                for (i, j) in contrainte_Liste:
                    if j == x or i == x:
                        file_L += [(i, j)]

        elapsed_time = time.time() - start_time
        if self.traceframe:
            self.traceframe.add_To_Trace("Fin de l'AC3", "out")
            self.traceframe.add_To_Trace(" Temps :" + str(elapsed_time) + "\n", "time")
        else:
            print "AC3 Temps :" + str(elapsed_time)

        return True

    def revise(self, x, y):
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
        if self.traceframe:
            self.traceframe.add_To_Trace("Debut revise de :" + str(x.lettres) + " et " + str(y.lettres) + "\n", "in")
        start_time = time.time()

        modif = False
        tmp = set()
        for mot in x.domaine:
            consistant = False
            for mot2 in y.domaine:
                if self.consistance((x, mot), (y, mot2)):
                    consistant = True
                    break
            if not consistant:
                if self.traceframe:
                    self.traceframe.add_To_Trace(
                        'mot :' + str(mot) + " supprimer du domaine de " + str(x) + " a cause de " + str(y) + "\n",
                        "curr")
                tmp.add(mot)
                modif = True

        x.remove(tmp)
        s = [i + " " for i in tmp]
        s = "".join(s)
        elapsed_time = time.time() - start_time
        if self.traceframe:
            self.traceframe.add_To_Trace("Les mots " + str(s) + " sont supprimés de " + str(x.lettres) + "\n", "curr")
            self.traceframe.add_To_Trace("Fin revise de :" + str(x.lettres) + " et " + str(y.lettres), "out")
            self.traceframe.add_To_Trace(" Temps :" + str(elapsed_time) + "\n", "time")
        #else:
        #    print " Temps :" + str(elapsed_time)
        return modif


    def revise2(self, x, y):
        """

        :param x:
        :param y:
        :return:
        """
        contraintsY = y.getContrainte(x)
        if not contraintsY:
            return False
        modif = False
        for indiceY in contraintsY:
            if indiceY == -1:
                # peut-être regarder la taille des domaines si D(y) == 1
                # D(x) = D(x)\D(y)
                # modif =
                modif = False
            else :
                yLettre = y.domaine2.getAllLettre(indiceY)
                bool = x.domaine2.updateFromContraintes(x.getContraintsXE(y), yLettre)
                modif =  bool
        return modif

    def consistance(self, (x, mot), (y, mot2)):

        if mot == mot2:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant ==\n", "err")
            return False

        crossPosX = [cont[1] for cont in x.contrainteListe if cont[0] is y]

        if (len(crossPosX) > 0):
            crossPosX = [item for item in crossPosX if item != -1]
        if not crossPosX:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Consistant \n", "curr")
            return True

        elif len(crossPosX) > 1:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant ???\n", "err")
            return False

        crossPosY = [cont[1] for cont in y.contrainteListe if cont[0] is x]

        if (len(crossPosY) > 0):
            crossPosY = [item for item in crossPosY if item != -1]
        if not crossPosY:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Consistant \n", "curr")
            return True

        if len(crossPosY) > 1:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant ???\n", "err")
            return False

        # print str(x)+" "+str(mot) + " end " + str(mot2) + " " + str(y) + " " + str(mot[crossPosX[0]] is mot2[crossPosY[0]])
        b = mot[crossPosX[0]] is mot2[crossPosY[0]]
        if b:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Consistant \n", "curr")
        else:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant Lettre\n", "err")
        return b

    def check_forward(self, xk, v, V):
        """
        consistant ← true
        pour chaque xj ∈ V \ {xk } et tant que consistant
            faire pour chaque v' ∈ Dj
                si {xk → v, xj → v'} non-consistant
                    alors Dj ← Dj \ {v'}
                fsi
            fait
        si Dj = ∅ alors consistant ← false
        retourner consistant
        """

        for xj in V:
            if not xj == xk:
                sup = set()
                for vv in xj.domaine:
                    if not self.consistance((xk, v), (xj, vv)):
                        sup.add(vv)
                xj.remove(sup)
                if not xj.domaine:
                    return False
        return True

    def forward_checking(self, V, i):
        """
        si V = ∅ alors i est une solution
        sinon
            choisir xk ∈ V
            faire pour tout v ∈ Dk
                sauvegarde(V \ {xk })
                si check-forward(xk , v, V) alors
                    forward-checking(V \ {xk }, i ∪ {xk → v})
                fsi
                restauration V \ {xk }
            fait
        fsi
        """

        if not V:
            self.res = i
            return i

        xk = V[0]
        for v in xk.domaine:
            if self.check_forward(xk, v, V[1:]):
                return self.forward_checking(V, i + [(xk, v)])

        return None

    def RAC(self, i, V):
        """
        si V = vide alors retourner la solution
        sinon
            choisir xk dans V
            faire pour tout v dans Dxk
                si i U (xk -> v) est localement consistant
                    alors RAC(i U (xk -> v), V \ {xk},D,C)
            fait
        fsi
        :param V:
        :param i:
        """
        if not V:
            if not self.res:
                self.res = i
            return i

        xk = self.heuristique_dom_mim(V)
        #print i, V
        V.remove(xk)

        for v in xk.domaine:
            if self.consistance_locale(i, (xk, v)):
                self.RAC(i + [(xk, v)], V[::])

        return None

    def consistance_locale(self, i, y):
        for x in i:
            if not self.consistance(x, y):
                return False
        return True

    def CBJ(self, V, i):
        '''

        '''
        if not V:
            if not self.res:
                self.res = i
            return i
        xk = self.heuristique_triviale(V)
        conflit = []
        nonBJ = True
        V.remove(xk)
        for v in xk.domaine:
            if not nonBJ:
                return conflit
            conflit_local = self.consistante(i + [(xk, v)])
            if not conflit_local:
                conflit_fils = self.CBJ(V[::], i + [(xk, v)])
                if xk in conflit_fils:
                    conflit += conflit_fils
                else:
                    conflit = conflit_fils
                    nonBJ = False
            conflit += conflit_local

    def consistante(self, inst):
        conflit = []
        for i in range(len(inst)):
            x1 = inst[i]
            for j in range(i + 1, len(inst)):
                x2 = inst[j]
                if not self.consistance(x1, x2):
                    conflit += [x1[0], x2[0]]
        return conflit

    def heuristique_triviale(self, V):
        return V[0]

    def heuristique_dom_mim(self, V):
        elemMin = [(len(V[0].domaine), 0)]
        for i in range(1, len(V)):
            if len(V[i].domaine) < elemMin[0][0]:
                elemMin = [(len(V[i].domaine), i)]
            elif len(V[i].domaine) == elemMin[0][0]:
                elemMin += [(len(V[i].domaine), i)]
        if len(elemMin) == 1:
            return V[elemMin[0][1]]
        else:
            return V[(random.choice(elemMin))[1]]

    def heuristique_contr_max(self, V):
        elemMax = [(len(V[0].contrainteListe), 0)]
        for i in range(1, len(V)):
            if len(V[i].contrainteListe) > elemMax[0][0]:
                elemMax = [(len(V[i].contrainteListe), i)]
            elif len(V[i].contrainteListe) == elemMax[0][0]:
                elemMax += [(len(V[i].contrainteListe), i)]
        if len(elemMax) == 1:
            return V[elemMax[0][1]]
        else:
            return V[(random.choice(elemMax))[1]]


    def heuristique_instance_max(self, V):
        """
        variable qui a le plus de contrainte avec les variables déjà instanciées
        :param V:
        :return:
        """
        pass
