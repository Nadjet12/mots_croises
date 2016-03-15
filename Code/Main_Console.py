#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from grille.Algos import Algo
from grille.Grille import Grille

Grille_Var = "./grillesVides/td3vide.mc"
Dictionnaire_Var = "./mots/td3.txt"
Algo_Var = "AC3"

#Grille_Var = "./grillesVides/C.mc"
#Dictionnaire_Var = "./mots/22600-mots-fr.txt"

if __name__ == "__main__":
    start_time = time.time()
    grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)
    elapsed_time = time.time() - start_time
    print "Creation grille " + Grille_Var.split("/")[-1] + " Temps :" + str(elapsed_time)

    algo = Algo(grille=grille, algo=Algo_Var)
    algo.start()

    #Attendre la fin du thread "Algo"
    algo.join()
    print
    print "Mots Verticaux :"
    for m in grille.mots_verticaux:
        m.printDomaine()
    print "Mots Horizontaux :"
    for m in grille.mots_horizontaux:
        m.printDomaine()