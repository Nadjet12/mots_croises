#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from grille.Algos import Algo
from grille.Grille import Grille

Grille_Var = "./grillesVides/td3vide.mc"
#Grille_Var = "./grillesVides/A.mc"
#Grille_Var = "./grillesVides/C.mc"
#Grille_Var = "./grillesVides/7.mc"
#Dictionnaire_Var = "./mots/850-mots-us.txt"
#Dictionnaire_Var = "./mots/test2.txt"
#Dictionnaire_Var = "./mots/test.txt"
#Dictionnaire_Var = "./mots/58000-mots-us.txt"
#Dictionnaire_Var = "./mots/135000-mots-fr.txt"
Dictionnaire_Var = "./mots/td32.txt"
#Algo_Var = "AC3"
Algo_Var = "FC_AC3"

if __name__ == "__main__":
    start_time = time.time()
    grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)
    elapsed_time = time.time() - start_time
    print "Creation grille " + Grille_Var.split("/")[-1] + " Temps :" + str(elapsed_time)
    print "Mots Verticaux :"
    for m in grille.mots_verticaux:
        print m
    print "Mots Horizontaux :"
    for m in grille.mots_horizontaux:
        print m


    algo = Algo(grille=grille, algo=Algo_Var)
    print "nbMot :" + str(grille.motSize())
    start_time = time.time()
    algo.start()

    # Attendre la fin du thread "Algo"
    algo.join()
    elapsed_time = time.time() - start_time
    print Algo_Var + " " + Grille_Var.split("/")[-1] + " Temps :" + str(elapsed_time)
    if algo.res:
        algo.grille.setResultat(algo.res)
        algo.grille.sauvegarder_grille("./grillesVides/td3Solution.mc")
        for i in algo.res:
            print i
    else:
        print "Pas de solution"
