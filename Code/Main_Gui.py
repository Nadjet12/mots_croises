#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import Tk

import time

from grille.Algos import Algo
from grille.Grille import Grille
from gui.Gui import Gui


Grille_Var = "./grillesVides/td3vide.mc"
#Grille_Var = "./grillesVides/A.mc"
#Dictionnaire_Var = "./mots/850-mots-us.txt"
#Dictionnaire_Var = "./mots/135000-mots-fr.txt"
Dictionnaire_Var = "./mots/td3.txt"
Algo_Var = "AC3"



if __name__ == "__main__":
    root = Tk()

    start_time = time.time()
    grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)
    elapsed_time = time.time() - start_time
    print "Creation grille " + Grille_Var.split("/")[-1] + " Temps :" + str(elapsed_time)
    algo = Algo(grille=grille, algo=Algo_Var)
    interface = Gui(master=root, root=root, algo=algo)
    interface.master.title("RP : Mots Croisés (Bourdache Nadjet Adequin Renaud)")
    interface.pack(fill="both", expand=True)

    interface.mainloop()
