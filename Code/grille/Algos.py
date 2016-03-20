# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 12:16:39 2016

@author: Nadjet BOURDACHE
"""
import threading
import time
import random
from copy import deepcopy
from types import NoneType

from grille import Grille
import Mot


class StoppableThread(object):
    pass


class Algo(threading.Thread):
    def __init__(self, queue=None, grille=None, traceframe=None, algo=None):
        #super(StoppableThread, self).__init__()
        threading.Thread.__init__(self)

        self.wait = False
        self.queue = queue
        self.grille = grille
        self.traceframe = traceframe
        self.algo = algo
        self.res = None
        self.fini = False
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        if self.algo is "AC3":
            bool = self.ac3()
            if self.queue:
                self.queue.put(bool)
        elif self.algo is "FC":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            #self.ac3()
            random.shuffle(liste)
            self.forward_checking(liste, [])
            if self.queue:
                self.queue.put(None)

        elif self.algo is "FC/AC3":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            self.ac3()
            random.shuffle(liste)
            self.forward_checking(liste, [])
            if self.queue:
                self.queue.put(None)

        elif self.algo is "CBJ":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            random.shuffle(liste)
            self.CBJ(liste, [])
            #if self.queue:
            #    self.queue.put(None)
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
            if self.revise2(x, y):
                '''
                print "Mots Verticaux :"
                for m in self.grille.mots_verticaux:
                    m.printDomaine()
                print "Mots Horizontaux :"
                for m in self.grille.mots_horizontaux:
                    m.printDomaine()
                '''
                if not x.domaine2:
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
        contraintsY = y.getContraintsX(x)
        if not contraintsY:
            return False
        modif = False
        for indiceY in contraintsY:
            if indiceY == -1:
                s = y.getDomaine()
                if len(s) == 1:
                    s = s.pop()
                    d = x.getDomaine()
                    if s in d:
                        d.remove(s)
                        try:
                            x.initDomaine(d)
                        except TypeError:
                            print '-----EXECPT'
                            print x
                            print y
                            print s
                            print x.getDomaine()
                        return len(x.getDomaine()) != 0
                # peut-être regarder la taille des domaines si D(y) == 1
                # D(x) = D(x)\D(y)
                # modif =
                modif = False
            else :
                yLettre = y.getAllLettre(indiceY)
                '''
                print 'avant'
                print "x :" + str(x)
                print "y :" + str(y)
                print "indiceX :" + str(x.getContraintsXE(y))
                print "indiceY " + str(indiceY)
                print "ylettre :" + str(yLettre)
                '''
                '''
                print '!= AVANT-----------------'
                print x
                print y
                print x.getContraintsXE(y)
                print indiceY
                print yLettre
                '''
                bool = x.updateFromContraintes(x.getContraintsXE(y), yLettre)
                '''
                print '!= APRES-----------------'
                print x
                print y
                #h = raw_input()
                '''
                '''
                print 'apres'
                print "x :" + str(x)
                print bool
                #print bool
                #x.printDomaineSize()
                '''
                modif =  bool
        return modif

    def consistance(self, (x, mot), (y, mot2)):

        if mot == mot2:
            #if self.traceframe:
            #    self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant ==\n", "err")
            return False

        crossPosX = [cont[1] for cont in x.contrainteListe if cont[0] is y]

        if (len(crossPosX) > 0):
            crossPosX = [item for item in crossPosX if item != -1]
        if not crossPosX:
            #if self.traceframe:
            #    self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Consistant \n", "curr")
            return True

        elif len(crossPosX) > 1:
            #if self.traceframe:
            #    self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant ???\n", "err")
            return False

        crossPosY = [cont[1] for cont in y.contrainteListe if cont[0] is x]

        if (len(crossPosY) > 0):
            crossPosY = [item for item in crossPosY if item != -1]
        if not crossPosY:
            #if self.traceframe:
            #    self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Consistant \n", "curr")
            return True

        if len(crossPosY) > 1:
            #if self.traceframe:
            #    self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant ???\n", "err")
            return False

        # print str(x)+" "+str(mot) + " end " + str(mot2) + " " + str(y) + " " + str(mot[crossPosX[0]] is mot2[crossPosY[0]])
        b = mot[crossPosX[0]] is mot2[crossPosY[0]]
        '''
        if b:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Consistant \n", "curr")
        else:
            if self.traceframe:
                self.traceframe.add_To_Trace(str(mot) + " et " + str(mot2) + " Non Consistant Lettre\n", "err")
        '''
        return b

    def check_forward2(self, xk, v, V):
        for xj in V:
            #print '--------------------------------'
            #print xk
            #print v
            #print xj
            contraintsY = xk.getContraintsX(xj)
            #print contraintsY
            if not contraintsY:
                continue
            else:
                for indiceY in contraintsY:
                    if indiceY == -1:
                        s = xj.getDomaine()
                        s = list(s)
                        if v in s:
                            s.remove(v)
                            if len(s) == 0:
                                return False
                            xj.initDomaine(s)
                        #print xj
                    else :
                        yLettre = v[indiceY]
                        xj.updateFromContraintes(xj.getContraintsXE(xk), yLettre)
                        #print xj
                        if len(xj.getDomaine()) == 0:
                            return False
            if len(xj.getDomaine()) == 0:
                return False
        return True


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
                for vv in xj.getDomaine():
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
        print len(V)
        if not V:
            #print i
            self.res = i
            self.wait = True
            if self.queue:
                self.queue.put(self.res)
            self.waitContinue()
            #print "fin"
            return

        xk = self.heuristique_instance_max(V, i)
        V.remove(xk)
        savedDom = []
        for v in V:
            savedDom += [(v, v.getDomaine())]

        for v in xk.get_Domaine():
            I = i[:] + [(xk, v)]
            if self.check_forward2(xk, v, V):
                self.forward_checking(V[:], I)

            for mot, dom in savedDom:
                mot.initDomaine(dom)
        #print 'BACK'
        return

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
            print i
            self.res = i
            self.wait = True
            if self.queue:
                self.queue.put(self.res)
            self.waitContinue()
            print "fin"
            return


        xk = self.heuristique_contr_max(V)
        print len(V)
        V.remove(xk)

        for v in xk.get_Domaine():

            if self.consistance_locale(i, (xk, v)):
                self.RAC(i + [(xk, v)], V[:])


    def consistance_locale(self, i, y):
        for x in i:
            if not self.consistance(x, y):
                return False
        return True

    def CBJ(self, V, i):
        print len(V)
        if not V:
            self.res = i
            self.wait = True
            if self.queue:
                self.queue.put(self.res)
            self.waitContinue()
            print "fin"
            return []


        xk = self.heuristique_instance_max(V, i)

        #print xk
        conflit = []
        nonBJ = True
        V.remove(xk)


        for v in xk.get_Domaine():
            if not nonBJ:
                return conflit
            I = i[:] + [(xk, v)]
            conflit_local = self.consistante(i, (xk, v))
            if not conflit_local:
                conflit_fils = self.CBJ(V[:], I)
                #print conflit_fils
                if xk in conflit_fils:
                    conflit += conflit_fils
                else:
                    conflit = conflit_fils
                    nonBJ = False
            conflit += conflit_local
        return conflit

    def CBJ2(self, V, i):
        print len(V)
        if not V:
            self.res = i
            self.wait = True
            if self.queue:
                self.queue.put(self.res)
            self.waitContinue()
            print "fin"
            return []


        xk = self.heuristique_instance_max(V, i)
        #print xk
        conflit = []
        nonBJ = True
        V.remove(xk)
        Dxk = list(xk.get_Domaine())[:]

        while Dxk and nonBJ:
            v = Dxk.pop()
            I = i[:] + [(xk, v)]
            conflit_local = self.consistante(i, (xk, v))
            if not conflit_local:
                conflit_fils = self.CBJ2(V[:], I)
                if xk in conflit_fils:
                    conflit = conflit_fils
                else:
                    conflit += conflit_fils
                    nonBJ = False
            else:
                conflit += conflit_local
        return conflit



    def consistante(self, inst, (xk, v)):
        conflit = []
        for y in inst:
            if not self.consistance(y, (xk, v)):
                conflit += [y[0]]
        return conflit

    def heuristique_triviale(self, V):
        return V[0]

    def heuristique_dom_mim(self, V):
        elemMin = [(len(V[0].get_Domaine()), 0)]
        for i in range(1, len(V)):
            if len(V[i].get_Domaine()) < elemMin[0][0]:
                elemMin = [(len(V[i].get_Domaine()), i)]
            elif len(V[i].get_Domaine()) == elemMin[0][0]:
                elemMin += [(len(V[i].get_Domaine()), i)]
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

    def getcontraintesNB(self, x, i):
        c = x.contrainteListe
        nb = 0
        if not i:
            return 0
        t = [v[0] for v in i]
        cc = [v[0] for v in c]
        for el in cc:
            if el in t:
                nb += 1
        return nb


    def heuristique_instance_max(self, V, inst):
        """
        variable qui a le plus de contrainte avec les variables déjà instanciées
        :param V:
        :return:
        """
        elemMax = [(self.getcontraintesNB(V[0], inst), 0)]
        for i in range(1, len(V)):
            nb = self.getcontraintesNB(V[i], inst)
            if  nb > elemMax[0][0]:
                elemMax = [(nb, i)]
            elif len(V[i].contrainteListe) == elemMax[0][0]:
                elemMax += [(nb, i)]
        if len(elemMax) == 1:
            return V[elemMax[0][1]]
        else:
           return V[(random.choice(elemMax))[1]]




        pass

    def waitContinue(self):
        while self.wait:
            pass
            #print "a"