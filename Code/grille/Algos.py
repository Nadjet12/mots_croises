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
    def __init__(self, queue=None, grille=None, traceframe=None, algoName=None, heuristique=None):
        threading.Thread.__init__(self)

        # Variables de test
        self.tempsOvertureGrille = 0
        self.timed = 0
        self.nbMotsTeste = 0
        self.queue = queue
        self.grille = grille
        self.traceframe = traceframe
        self.algoName = algoName
        self.res = None

        if heuristique:
            self.heur = heuristique
        else:
            self.heur = self.heuristique_dom_mim

        # Variable de Thread
        self.pause_cond = threading.Condition(threading.Lock())
        self.paused = False
        self._stop = threading.Event()
        self.hasRun = False
        self.fin = False

    def setQueue(self, queue):
        self.queue = queue

    def setAlgoName(self, name):
        self.algoName = name

    def setGrille(self, grille):
        self.grille = grille

    def send_to_Trace(self, mess, mode):
        if self.traceframe:
            self.traceframe.add_To_Trace(mess, mode)
        else:
            print mess

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def pause(self):
        self.paused = True
        self.pause_cond.acquire()

    def resume(self):
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

    def sendResult(self, resultat):
        if self.queue:
            self.queue.put(resultat)

    def run(self):
        self.hasRun = True
        if self.algoName is "AC3":
            bool = self.ac3()
            self.sendResult(bool)

        elif self.algoName is "FC":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            self.forward_checking(liste, [])

            # Pas ou plus de resultats
            self.sendResult(None)

        elif self.algoName is "FC_AC3":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            self.ac3()
            self.forward_checking(liste, [])

            # Pas ou plus de resultats
            self.sendResult(None)

        elif self.algoName is "CBJ":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            #self.ac3()
            self.CBJ(liste, [])
            print self.nbMotsTeste

            # Pas ou plus de resultats
            self.sendResult(None)

        elif self.algoName is "VAL":
            pass
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            self.branch_bound(liste)

            # Pas ou plus de resultats
            self.sendResult(None)
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
        self.send_to_Trace("Debut de l'AC3\n", 'in')
        contrainte_Liste = self.grille.getContraintes()
        file_L = contrainte_Liste[::]
        while file_L:
            (x, y) = file_L.pop(0)
            if self.revise(x, y):
                if len(x.getDomaine()) == 0:
                    return False
                for (i, j) in contrainte_Liste:
                    if j == x or i == x:
                        file_L += [(i, j)]

        elapsed_time = time.time() - start_time
        self.send_to_Trace("Fin de l'AC3 : " + str(nbMot-self.grille.get_Domaines_Sizes()) + " Mots ont été supprimés", "out")
        self.send_to_Trace(" Temps :" + str(elapsed_time) + "\n", "time")


        return True

    def revise(self, x, y):
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
            return False

        crossPosX = [cont[1] for cont in x.contrainteListe if cont[0] is y]

        if (len(crossPosX) > 0):
            crossPosX = [item for item in crossPosX if item != -1]
        if not crossPosX:
            return True

        elif len(crossPosX) > 1:
            return False

        crossPosY = [cont[1] for cont in y.contrainteListe if cont[0] is x]

        if (len(crossPosY) > 0):
            crossPosY = [item for item in crossPosY if item != -1]
        if not crossPosY:
            return True

        if len(crossPosY) > 1:
            return False

        b = mot[crossPosX[0]] is mot2[crossPosY[0]]
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
            self.send_to_Trace("Debut du Forward Checking :\n", "in")
            self.timed = time.time()

        if not V:
            self.timed = time.time() - self.timed
            self.send_to_Trace("Fin du Forward Checking ", "out")
            self.send_to_Trace(" Temps :" + str(self.timed) + "\n", "time")
            self.res = i
            self.sendResult(self.res)
            #self.fin = True
            self.pause()
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                self.timed = time.time()


            return

        xk = self.heur(V, i)
        V.remove(xk)
        savedDom = []
        for v in V:
            savedDom += [(v, v.getDomaine(), len(v.getDomaine()))]

        for v in xk.getDomaine():
            self.nbMotsTeste +=1

            print self.nbMotsTeste
            I = i[:] + [(xk, v)]
            if self.check_forward2(xk, v, V):
                self.forward_checking(V[:], I)
            #if self.fin:
            #        return
            for mot, dom, taille in savedDom:
                mot.initDomaine(dom)
        return

    def consistance_locale(self, i, y):
        for x in i:
            if not self.consistance(x, y):
                return False
        return True

    def CBJ(self, V, i, it=1):
        print 'itération =' + str(it)
        if self.timed == 0:
            self.send_to_Trace("Debut du Conflict Back Jumping :\n", "in")
            self.timed = time.time()

        if not V:
            self.timed = time.time() - self.timed
            self.send_to_Trace("Fin du Conflict Back Jumping ", "out")
            self.send_to_Trace(" Temps :" + str(self.timed) + "\n", "time")
            self.res = i
            self.sendResult(self.res)
            #self.fin = True
            self.pause()
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                self.timed = time.time()
            return []


        xk = self.heuristique_instance_max(V, i)
        conflit = []
        nonBJ = True
        V.remove(xk)
        savedDom = []
        #print 'xk choisi :' +str(xk) + " : " +str(len(xk.getDomaine()))
        Dxk = xk.getDomaine()[:]
        nbMotsTeste = 0
        while Dxk and nonBJ:
            self.nbMotsTeste +=1
            nbMotsTeste +=1
            #print nbMotsTeste
            v = Dxk.pop()
            I = i[:] + [(xk, v)]
            conflit_local = self.consistante(i, (xk, v))
            if not conflit_local:
                #print 'Consistant ' + v
                conflit_fils = self.CBJ(V[:], I, it=it+1)
                #print "retour du cbj id :" + str(xk.id) + "  conflitfils" + str(conflit_fils)
                if xk.id in conflit_fils: #and len(conflit_fils) > 1:
                    #print 'xk in conflit fils > 1 ' +str(xk.id)
                    conflit_fils.remove(xk.id)
                    conflit += conflit_fils
                    conflit = list(set(conflit))
                    #nonBJ = False
                else:
                    conflit = conflit_fils
                    nonBJ = False
                    #print "xk not in conflit fils " + str(xk.id)
                '''
                elif xk.id in conflit_fils:
                    print 'xk in conflit fils == 1 ' +str(xk.id)
                    conflit_fils.remove(xk.id)
                    conflit = conflit_fils
                    conflit = list(set(conflit))
                '''

            else:
                conflit += conflit_local
                conflit = list(set(conflit))
                #print 'conflit local :' + str(conflit) + "   mot :" + v
        #if it == 1:
        #    print 'fin Whhile it :' +str(it) + " mot testé "+ str(nbMotsTeste) + "  xk :" + str(xk)
        return conflit

    def CBJ2(self, V, i, it=1):
        print 'itération =' + str(it)
        if self.timed == 0:
            self.send_to_Trace("Debut du Conflict Back Jumping :\n", "in")
            self.timed = time.time()

        if not V:
            self.timed = time.time() - self.timed
            self.send_to_Trace("Fin du Conflict Back Jumping ", "out")
            self.send_to_Trace(" Temps :" + str(self.timed) + "\n", "time")
            self.res = i
            self.sendResult(self.res)
            #self.fin = True
            self.pause()
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                self.timed = time.time()
            return []


        xk = self.heuristique_instance_max(V, i)
        conflit = []
        nonBJ = True
        V.remove(xk)
        print 'xk choisi :' +str(xk) + " : " +str(len(xk.getDomaine()))
        savedDom = []
        for v in V:
            savedDom += [(v, v.getDomaine(), len(v.getDomaine()))]

        Dxk = xk.getDomaine()[:]
        h = 0
        while Dxk and nonBJ:
            self.nbMotsTeste +=1
            h+=1
            v = Dxk.pop()
            I = i[:] + [(xk, v)]
            print 'AVANT CF---------------'
            self.printV(V)

            if self.check_forward2(xk, v, V):
                print 'APRES CF--------------'
                self.printV(V)
                conflit_local = self.consistante(i, (xk, v))
                if not conflit_local:
                    print 'Consistant'
                    conflit_fils = self.CBJ2(V[:], I, it=it+1)
                    if xk.id in conflit_fils:
                        print 'xk in conflit fils ' +str(xk.id)
                        conflit += conflit_fils
                    else:
                        conflit = conflit_fils
                        nonBJ = False
                        print "xk not in conflit fils " + str(xk.id)
                else:
                    conflit += conflit_local

            for mot, dom, taille in savedDom:
                mot.initDomaine(dom)
            self.printV(V)
            print "mot restant a tester " + str(len(Dxk)-h)
        print 'fin Whhile it :' +str(it)
        print conflit
        return conflit

    def printV(self, V):
        for mot in V:
            print mot

    def consistante(self, inst, (xk, v)):
        conflit = set()
        for y in inst:
            if not self.consistance(y, (xk, v)):
                #print 'non consistant --------'
                #print str(y)
                #print str((xk, v))
                #print '-------------'
                conflit.add(y[0].id)
        return list(conflit)

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

    def branch_bound(self, V):
        if self.timed == 0:
            self.send_to_Trace("Debut du Branch & Bound :\n", "in")
            self.timed = time.time()

        arbre = Arbre(V)
        sol = arbre.update()
        while not sol:
            sol = arbre.update()

        solution = []
        while not sol is None:
            solution += [(sol.motObj, sol.mot, sol.value)]
            sol = sol.pere
        self.timed = time.time() - self.timed
        self.send_to_Trace("Fin du Branch & Bound ", "out")
        self.send_to_Trace(" Temps :" + str(self.timed) + "\n", "time")
        self.res = solution
        self.sendResult(self.res)
        #self.fin = True
        self.pause()
        with self.pause_cond:
            while self.paused:
                self.pause_cond.wait()
            self.timed = time.time()


