# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 12:16:39 2016

@author: Nadjet BOURDACHE
"""
import threading
import time
import random
from Arbre import Arbre

class StoppableThread(object):
    pass


class Algo(threading.Thread):
    def __init__(self, queue=None, grille=None, traceframe=None, algo=None, heuristique=None):
        #super(StoppableThread, self).__init__()
        threading.Thread.__init__(self)
        self.tempsOvertureGrille = 0
        self.timed = 0
        self.nbMotsTeste = 0
        self.queue = queue
        self.grille = grille
        self.traceframe = traceframe
        self.algo = algo
        self.res = None
        self.heur = self.heuristique_dom_mim

        self.pause_cond = threading.Condition(threading.Lock())
        self.paused = False
        self._stop = threading.Event()
        self.hasRun = False
        self.fin = False



    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


    def pause(self):
        self.paused = True
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        self.pause_cond.acquire()

    #should just resume the thread
    def resume(self):
        self.paused = False
        # Notify so thread will wake after lock released
        self.pause_cond.notify()
        # Now release the lock
        self.pause_cond.release()

    def run(self):
        self.hasRun = True
        if self.algo is "AC3":
            bool = self.ac3()
            if self.queue:
                self.queue.put(bool)
        elif self.algo is "FC":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            random.shuffle(liste)
            self.forward_checking(liste, [])
            if self.queue:
                self.queue.put(None)

        elif self.algo is "FC_AC3":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            taileDom = self.grille.get_Domaines_Sizes()
            print "Taille des domaines : " + str(taileDom) + " mots"
            #start_time = time.time()
            self.ac3()
            print "Mots Verticaux :"
            for m in self.grille.mots_verticaux:
                print m
            print "Mots Horizontaux :"
            for m in self.grille.mots_horizontaux:
                print m
            #elapsed_time = time.time() - start_time
            #print "AC3 Temps :" + str(elapsed_time)
            taileDom2 = self.grille.get_Domaines_Sizes()
            print "Taille des domaines : " + str(taileDom2) + " mots\nReduit de :" + str(taileDom-taileDom2) + " mots"

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

        nbMot = self.grille.get_Domaines_Sizes()
        start_time = time.time()
        if self.traceframe:
            self.traceframe.add_To_Trace("Debut de l'AC3\n", 'in')
        contrainte_Liste = self.grille.getContraintes()
        file_L = contrainte_Liste[::]
        while file_L:
            (x, y) = file_L.pop(0)
            if self.revise2(x, y):
                if len(x.getDomaine()) == 0:
                    return False
                for (i, j) in contrainte_Liste:
                    if j == x or i == x:
                        file_L += [(i, j)]

        elapsed_time = time.time() - start_time
        if self.traceframe:
            self.traceframe.add_To_Trace("Fin de l'AC3 : " + str(nbMot-self.grille.get_Domaines_Sizes()) + " Mots ont été supprimés", "out")
            self.traceframe.add_To_Trace(" Temps :" + str(elapsed_time) + "\n", "time")
        else:
            #print "AC3 Temps :" + str(elapsed_time)
            pass

        return True

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
                    s = s[0]
                    d = x.getDomaine()
                    if s in d:
                        d.remove(s)
                        x.removeMotFromDomaine(s)
                        if len(x.getDomaine()) == 0:
                            #si le domaine de x est 0 on arete et on dis que c'est modifié
                            return True
                modif = False
            else :
                yLettre = y.getAllLettre(indiceY)
                nb = len(x.getDomaine())
                bool = x.updateFromContraintes(x.getContraintsXE(y), yLettre)

                nb -= len(x.getDomaine())
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
            contraintsY = xk.getContraintsX(xj)
            for indiceY in contraintsY:
                if indiceY == -1:
                    s = xj.getDomaine()
                    s = list(s)
                    if v in s:
                        s.remove(v)
                        if len(s) == 0:
                            return False
                        xj.removeMotFromDomaine(v)
                else :
                    yLettre = v[indiceY]
                    xj.updateFromContraintes(xj.getContraintsXE(xk), yLettre)
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
        if self.timed == 0:
            if self.traceframe:
                self.traceframe.add_To_Trace("Debut du Forward Checking :\n", "in")
            self.timed = time.time()

        if not V:
            self.timed = time.time() - self.timed
            print self.timed
            if self.traceframe:
                self.traceframe.add_To_Trace("Fin du Forward Checking ", "out")
                self.traceframe.add_To_Trace(" Temps :" + str(self.timed) + "\n", "time")
            print i
            self.res = i
            if self.queue:
                self.queue.put(self.res)
            self.fin = True
            #self.pause()
            #with self.pause_cond:
            #    while self.paused:
            #        self.pause_cond.wait()
            #    self.timed = time.time()


            return

        xk = self.heur(V, i)
        V.remove(xk)
        savedDom = []
        for v in V:
            savedDom += [(v, v.getDomaine(), len(v.getDomaine()))]

        for v in xk.getDomaine():
            self.nbMotsTeste +=1
            #print self.nbMotsTeste
            I = i[:] + [(xk, v)]
            if self.check_forward2(xk, v, V):
                self.forward_checking(V[:], I)
            if self.fin:
                    return
            for mot, dom, taille in savedDom:
                mot.initDomaine(dom)
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
            #self.waitContinue()
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


        xk = self.heur(V, i)
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

    def heuristique_triviale(self, V, i):
        return V[0]

    def heuristique_dom_mim(self, V, i):
        elemMin = [(len(V[0].getDomaine()), 0)]
        for i in range(1, len(V)):
            dom = len(V[i].getDomaine())
            if dom < elemMin[0][0]:
                elemMin = [(dom, i)]
            elif dom == elemMin[0][0]:
                elemMin += [(dom, i)]
        if len(elemMin) == 1:
            return V[elemMin[0][1]]
        else:
            return V[(random.choice(elemMin))[1]]

    def heuristique_contr_max(self, V, i):
        elemMax = [(len(V[0].contrainteListe), 0)]
        for i in range(1, len(V)):
            contr = len(V[i].contrainteListe)
            if contr > elemMax[0][0]:
                elemMax = [(contr, i)]
            elif contr == elemMax[0][0]:
                elemMax += [(contr, i)]
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


    def branch_bound(self, V, i):
        if not V:
            return i
        arbre = Arbre(V)
        while not arbre.update():
            continue
        return arbre.solution