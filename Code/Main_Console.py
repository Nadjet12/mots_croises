#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from grille.Algos import Algo
from grille.Grille import Grille

Grille_Var = "./grillesVides/td3vide.mc"
# Grille_Var = "./grillesVides/A.mc"
# Dictionnaire_Var = "./mots/850-mots-us.txt"
# Dictionnaire_Var = "./mots/22600-mots-fr.txt"
Dictionnaire_Var = "./mots/td3.txt"
Algo_Var = "RAC"

if __name__ == "__main__":
    start_time = time.time()
    grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)
    elapsed_time = time.time() - start_time
    print "Creation grille " + Grille_Var.split("/")[-1] + " Temps :" + str(elapsed_time)
    algo = Algo(grille=grille, algo=Algo_Var)
    algo.start()

    # Attendre la fin du thread "Algo"
    algo.join()

    print algo.res
    print "Mots Verticaux :"
    for m in grille.mots_verticaux:
        m.printDomaineSize()
    print "Mots Horizontaux :"
    for m in grille.mots_horizontaux:
        m.printDomaineSize()
