#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import Tk

import time

from grille.Algos import Algo
from grille.Grille import Grille
from gui.Gui import Gui


Grille_Var = "./grillesVides/td3vide.mc"
#Grille_Var = "./grillesVides/A.mc"
# Grille_Var = "./grillesVides/C.mc"
#Grille_Var = "./grillesVides/7.mc"
Dictionnaire_Var = "./mots/850-mots-us.txt"
#Dictionnaire_Var = "./mots/test2.txt"
#Dictionnaire_Var = "./mots/test2.txt"
#Dictionnaire_Var = "./mots/58000-mots-us.txt"
#Dictionnaire_Var = "./mots/135000-mots-fr.txt"
#Dictionnaire_Var = "./mots/td3.txt"
#Algo_Var = "AC3"
Algo_Var = "RAC"



if __name__ == "__main__":
    root = Tk()

    start_time = time.time()
    #grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)
    elapsed_time = time.time() - start_time
    print "Creation grille " + Grille_Var.split("/")[-1] + " Temps :" + str(elapsed_time)
    algo = Algo(grille=None, algoName="AC3")
    interface = Gui(master=root, root=root, algo=algo)
    interface.master.title("RP : Mots Croisés (Bourdache Nadjet, Adequin Renaud)")
    interface.pack(fill="both", expand=True)

    interface.mainloop()
