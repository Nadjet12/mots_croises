#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from grille import Algos
from grille.Grille import Grille

Grille_Var = "./grillesVides/C.mc"
Dictionnaire_Var = "./mots/58000-mots-us.txt"

if __name__ == "__main__":
    start_time = time.time()
    grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)
    elapsed_time = time.time() - start_time
    print "Creation grille " + Grille_Var.split("/")[-1] + " Temps :" + str(elapsed_time)

    Algos.ac3(grille, None)

    for m in grille.mots_verticaux:
        m.printDomaine()
    for m in grille.mots_horizontaux:
        m.printDomaine()