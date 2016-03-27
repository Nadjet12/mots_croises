#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from grille.Algos import Algo
from grille.Grille import Grille

#Grille_Var = "./grillesVides/td3vide.mc"
#Grille_Var = "./grillesVides/A.mc"
#Grille_Var = "./grillesVides/B.mc"
#Grille_Var = "./grillesVides/C.mc"
#Grille_Var = "./grillesVides/7.mc"
#Dictionnaire_Var = "./mots/850-mots-us.txt"
#Dictionnaire_Var = "./mots/22600-mots-fr.txt"
#Dictionnaire_Var = "./mots/test2.txt"
#Dictionnaire_Var = "./mots/test.txt"
#Dictionnaire_Var = "./mots/58000-mots-us.txt"
#Dictionnaire_Var = "./mots/135000-mots-fr.txt"
#Dictionnaire_Var = "./mots/td32.txt"
#Algo_Var = "AC3"
#Algo_Var = "FC"


if __name__ == "__main__":


    DICT = ["./mots/850-mots-us.txt", "./mots/22600-mots-fr.txt","./mots/58000-mots-us.txt", "./mots/133000-mots-us.txt", "./mots/135000-mots-fr.txt"]
    GRILLE = ["./grillesVides/A.mc", "./grillesVides/B.mc", "./grillesVides/C.mc"]
    ALGO = ["AC3", "FC", "FC_AC3"]
    #for Algo_Var in ALGO:
        #for Grille_Var in GRILLE:

            #for Dictionnaire_Var in DICT:
                #grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)
Algo_Var = "FC"
Dictionnaire_Var = "./mots/133000-mots-us.txt"
Grille_Var = "./grillesVides/C.mc"
grille = Grille(filePath=Grille_Var, dictionnaire=Dictionnaire_Var)


#algo = Algo(grille=grille, algo=Algo_Var)
algo = Algo(grille=grille, algo=Algo_Var)

#Heuristique = algo.heuristique_dom_mim
Heuristique = algo.heuristique_contr_max
#Heuristique = algo.heuristique_instance_max
#Heuristique = algo.heuristique_triviale

#fichier = open("./temps_"+Algo_Var+"_"+Grille_Var.split("/")[-1][:-3]+"_"+str(len(grille.mots_horizontaux+grille.mots_verticaux))+".stat", "a")
fichier = open("./Nb_Mot_"+Algo_Var+"_"+Grille_Var.split("/")[-1][:-3]+".stat", "a")
algo.heur = Heuristique
#fichier.write(Dictionnaire_Var.split("/")[-1][:-4])
fichier.write(str(Heuristique.__name__))
fichier.write("\t")
start_time = time.time()
algo.start()

# Attendre la fin du thread "Algo"
algo.join()
print algo.nbMotsTeste
end_time= time.time() - start_time
#fichier.write(str(end_time))
print end_time
fichier.write(str(algo.nbMotsTeste))
fichier.write("\n")
fichier.close()
#print 'Fin '+ "temps_"+Algo_Var+"_"+Grille_Var.split("/")[-1][:-3]+"_"+str(len(grille.mots_horizontaux+grille.mots_verticaux))
#print 'Fin '+ "temps_"+Algo_Var+"_"+Grille_Var.split("/")[-1][:-3]+"_"+str(len(grille.mots_horizontaux+grille.mots_verticaux))
