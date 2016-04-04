# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 12.mc:16:39 2016

@author: Renaud ADEQUIN & Nadjet BOURDACHE
"""
import threading
import time
import random
from Tkinter import TclError

from Arbre import Arbre

class StoppableThread(object):
    pass


class Algo(threading.Thread):

    def __init__(self, queue=None, grille=None, traceframe=None, algoName=None, heuristique=None, stat=False):

        threading.Thread.__init__(self)

        # Variables de test
        self.stat = stat
        self.tempsOvertureGrille = 0
        self.timed = 0
        self.nbMotsTeste = 0
        self.queue = queue
        self.grille = grille
        self.traceframe = traceframe
        self.algoName = algoName
        self.res = None

        # Si on ne définit pas d'heuristique, l'heuristique du domaine min est prise par défaut
        if heuristique:
            self.heur = heuristique
        else:
            self.heur = self.heuristique_dom_mim

        # Variables de Thread
        self.pause_cond = threading.Condition(threading.Lock())
        self.paused = False
        self._stop = threading.Event()
        self.hasRun = False
        self.fin = False


    # Fonctions de gestion des algos

    def setQueue(self, queue):
        self.queue = queue

    def setAlgoName(self, name):
        self.algoName = name

    def setGrille(self, grille):
        self.grille = grille

    def send_to_Trace(self, mess, mode):
        try:
            if self.traceframe:
                self.traceframe.add_To_Trace(mess, mode)
            else:
                pass
        except TclError:
            print 'TclError'

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


    # Lancement de l'algo

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
            bool = self.ac3()
            self.sendResult(('AC3', bool))
            if bool :
                self.forward_checking(liste, [])

            # Pas ou plus de resultats
            self.sendResult(None)

        elif self.algoName is "CBJ_AC3":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            bool = self.ac3()
            self.sendResult(('AC3', bool))
            if bool :
                self.CBJ(liste, [])

            # Pas ou plus de resultats
            self.sendResult(None)
        elif self.algoName is "CBJ":
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            self.CBJ(liste, [])

            # Pas ou plus de resultats
            self.sendResult(None)

        elif self.algoName is "VAL":
            pass
            liste =  self.grille.mots_horizontaux + self.grille.mots_verticaux
            bool = self.ac3()
            self.sendResult(('AC3', bool))
            if bool :
                self.branch_bound(liste)

            # Pas ou plus de resultats
            self.sendResult(None)
        else:
            print "Error"


    def waitContinue(self):
        while self.wait:
            pass


    """********************************* Algorithmes de filtrages et de réolutions ****************************"""

    # Filtrage AC3

    def ac3(self):

        nbMot = self.grille.get_Domaines_Sizes()
        start_time = time.time()
        self.send_to_Trace("Debut de l'AC3\n", 'in')
        contrainte_Liste = self.grille.getContraintes()
        file_L = contrainte_Liste[::]

        # On parcours la totalité de la liste des contraintes de la grille
        while file_L:
            (x, y) = file_L.pop(0)
            if self.revise(x, y):
                # Si le domaine de x a été modifié, on vérifie qu'il n'est pas vide
                if len(x.getDomaine()) == 0:
                    elapsed_time = time.time() - start_time
                    self.send_to_Trace("Fin de l'AC3 : Non Consistant", "out")
                    self.send_to_Trace(" Temps :" + str(elapsed_time) + "\n", "time")
                    return False
                # Sinon, on ajoute à la liste de contraintes tous les mots directement liée à x par une contrainte
                for (i, j) in contrainte_Liste:
                    if j == x:
                        file_L += [(i, j)]

        # Affichage du temps d'exécution et du nombre de mots qui ont été supprimé des domaines
        elapsed_time = time.time() - start_time
        self.send_to_Trace("Fin de l'AC3 : " + str(nbMot-self.grille.get_Domaines_Sizes()) + " Mots ont été supprimés", "out")
        self.send_to_Trace(" Temps :" + str(elapsed_time) + "\n", "time")

        return True


    # Fonction "revise" utilisée dans l'AC3

    def revise(self, x, y):

        # S'il n y a pas de contraintes entre x et y pas de modification
        contraintsY = y.getContraintsX(x)
        if not contraintsY:
            return False
        modif = False

        # S'il y en a, on parcours la liste des contraintes pour voir s'il y a des
        # modifications à faire sur les domaines
        for indiceY in contraintsY:
            # Si la contrainte est liée à la taille des mots (x et y ont la même taille)
            if indiceY == -1:
                s = y.getDomaine()
                if len(s) == 1:
                    s = s[0]
                    d = x.getDomaine()
                    if s in d:
                        d.remove(s)
                        x.removeMotFromDomaine(s)
                        if len(x.getDomaine()) == 0:
                            # Si la taille du domaine de x est nulle on arête et on dis que c'est modifié
                            return True
                modif |= False
            # Si la contrainte est liée au fait que x et y se croisent
            else :
                yLettre = y.getAllLettre(indiceY)
                nb = len(x.getDomaine())
                bool = x.updateFromContraintes(x.getContraintsXE(y), yLettre)

                nb -= len(x.getDomaine())
                modif |=  bool
        return modif


    # Vérification de la consistance de l'instanciation qui consiste à affecter mot à c et mot2 à y

    def consistance(self, (x, mot), (y, mot2)):

        # Si les deux mots x et y ont la même valeur, l'instanciation n'est pas consistante

        if mot == mot2:
            return False

        # On récupère la listes de toutes les positions auxquelles y croise x
        # Cette valeur vaut -1 si x et y sont liée par une contrainte d'égalité des tailles de x et y

        crossPosX = [cont[1] for cont in x.contrainteListe if cont[0] is y]

        if (len(crossPosX) > 0):
            crossPosX = [item for item in crossPosX if item != -1]
        # Une fois qu'on a supprimé les contraintes d'égalité, si la liste est vide => instanciation consistante
        if not crossPosX:
            return True

        # On récupère la listes de toutes les positions auxquelles x croise y

        crossPosY = [cont[1] for cont in y.contrainteListe if cont[0] is x]

        if (len(crossPosY) > 0):
            crossPosY = [item for item in crossPosY if item != -1]
        if not crossPosY:
            return True

        # On vérifie que la case qui se situe au croisement de x et y possède la même valeur pour les deux mots
        b = mot[crossPosX[0]] is mot2[crossPosY[0]]

        # On renvoie le résultat
        return b

    # Filtrage par check forward
    def check_forward(self, xk, v, V):
        for xj in V:
            contraintsY = xk.getContraintsX(xj)
            for indiceY in contraintsY:
                # Contrainte d'égalité des taille de x et y
                if indiceY == -1:
                    s = xj.getDomaine()
                    s = list(s)
                    if v in s:
                        s.remove(v)
                        if len(s) == 0:
                            return False
                        xj.removeMotFromDomaine(v)
                # Contrainte de croisement de x et y
                else :
                    yLettre = v[indiceY]
                    xj.updateFromContraintes(xj.getContraintsXE(xk), yLettre)
                    # Si après modification le domaine est vide, l'instanciation n'est pas bonne
                    if len(xj.getDomaine()) == 0:
                        return False
            # Si après modification le domaine est vide, l'instanciation n'est pas bonne
            if len(xj.getDomaine()) == 0:
                return False
        return True


    # Résolution par FC
    def forward_checking(self, V, i):

        #Affichage d'un message au début de l'algo
        if self.timed == 0:
            self.send_to_Trace("Debut du Forward Checking :\n", "in")
            self.timed = time.time()

        # Lorsqu'il n'y a plus de variables à instancier, l'algo se termine et on affiche le résultat et le temps de calcul
        if not V:
            self.timed = time.time() - self.timed
            self.send_to_Trace("Fin du Forward Checking ", "out")
            self.send_to_Trace(" Temps :" + str(self.timed) + "\n", "time")
            self.res = i
            self.sendResult(self.res)
            if self.stat:
                self.fin = True
                return
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
            I = i[:] + [(xk, v)]
            if self.check_forward(xk, v, V):
                self.forward_checking(V[:], I)
                if self.stat:
                    if self.fin:
                        return
            for mot, dom, taille in savedDom:
                mot.initDomaine(dom)
        return

    # consistance_local vérifie si l'instanciation est consistante par rapport à y
    def consistance_locale(self, i, y):
        for x in i:
            if not self.consistance(x, y):
                return False
        return True

    # Résolution par CBJ

    def CBJ(self, V, i, it=1):
        prev = []
        if i:
            prev = [i[-1][0].id]

        # Affichage au début de l'algo
        if self.timed == 0:
            self.send_to_Trace("Debut du Conflict Back Jumping :\n", "in")
            self.timed = time.time()

        # Lorsqu'il n'y a plus de variables à instancier, l'algo se termine et on affiche le résultat et le temps de calcul
        if not V:
            self.timed = time.time() - self.timed

            self.send_to_Trace("Fin du Conflict Back Jumping ", "out")
            self.send_to_Trace(" Temps :" + str(self.timed) + "\n", "time")
            self.res = i
            self.sendResult(self.res)
            self.res = i
            self.sendResult(self.res)
            if self.stat:
                self.fin = True
                return
            self.pause()
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                self.timed = time.time()


            return prev

        # Résolution s'il reste des variables à instancier

        xk = self.heur(V, i)
        conflit = []
        nonBJ = True
        V.remove(xk)
        savedDom = []
        for v in V:
            savedDom += [(v, v.getDomaine(), len(v.getDomaine()))]
        Dxk = xk.getDomaine()[:]
        while Dxk and nonBJ:
            v = Dxk.pop()
            I = i[:] + [(xk, v)]
            if self.check_forward(xk, v, V):
                conflit_local = self.consistante(i, (xk, v))
                if not conflit_local:
                    conflit_fils = self.CBJ(V[:], I, it=it+1)
                    if self.stat:
                        if self.fin:
                            return
                    if xk.id in conflit_fils:
                        conflit += conflit_fils
                        conflit = list(set(conflit))
                    else:
                        conflit = conflit_fils
                        nonBJ = False
                else:
                    conflit = conflit_local
                    conflit = list(set(conflit))
            for mot, dom, taille in savedDom:
                mot.initDomaine(dom)
        if xk.id in conflit:
            conflit.remove(xk.id)
        if not conflit:
            conflit += prev
            conflit = list(set(conflit))
        return conflit


    # Vérification de la consistance de l'instanciation courante et de l'affectation du mot v à la variable xk
    def consistante(self, inst, (xk, v)):
        conflit = set()
        for y in inst:
            if not self.consistance(y, (xk, v)):
                conflit.add(y[0].id)
        return list(conflit)


    """************************** Heuristiques ***************************************"""

    # Premier élément de la liste des variables à instancier
    def heuristique_triviale(self, V, i):
        return V[0]

    # Variable ayant le domaine le plus petit dans l'instanciation courante
    def heuristique_dom_mim(self, V, inst, rand=True):
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
            if not rand:
                l = [V[k] for h,k in elemMin]
                return self.heuristique_contr_max(l, inst, False)
            return V[(random.choice(elemMin))[1]]


    # Variable ayant un nombre maximum de contraintes avec les autres variables
    def heuristique_contr_max(self, V, inst, rand=True):
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
            if not rand:
                l = [V[k] for h,k in elemMax]
                return self.heuristique_instance_max(l, inst, False)
            return V[(random.choice(elemMax))[1]]

    # Calcul du nombre de contraintes qu'a x avec les variables de l'instanciation courante
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


    def heuristique_instance_max(self, V, inst, rand=False):

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



    """ ***************************** Algo de Branch & Bound pour CSPs valués *************************** """

    def branch_bound(self, V):

        # Affichage au début de l'algo
        if self.timed == 0:
            self.send_to_Trace("Debut du Branch & Bound :\n", "in")
            self.timed = time.time()

        # Initialisation de l'algo
        arbre = Arbre(V, self)

        # Initialisation de la liste des feuilles
        sol = arbre.update()
        # Tant qu'on a pas de solution, on met à jour la liste des feuilles
        while not sol:
            sol = arbre.update()
            if isinstance(sol, str):
                print sol
                return

        # Construction de la solution entière à partir de la feuille
        solution = []
        while sol:
            solution += [(sol.motObj, sol.mot, sol.value)]
            sol = sol.pere

        # Affichage de la solution et du temps de calcul
        self.timed = time.time() - self.timed
        self.send_to_Trace("Fin du Branch & Bound ", "out")
        self.send_to_Trace(" Temps :" + str(self.timed) + "\n", "time")
        self.res = solution
        self.sendResult(self.res)

        self.pause()
        with self.pause_cond:
            while self.paused:
                self.pause_cond.wait()
            self.timed = time.time()
