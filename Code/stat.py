# -*- coding: utf-8 -*-
import time
from grille.Grille import Grille

from grille.Dictionnaire import Dico

from grille.Algos import Algo

DICO_PATH = '../Data/mots/'
GRILLEVIDE_PATH = '../Data/grillesVides/'


PATHSAVE = '../Stat/stat/'
if __name__ == "__main__":

    DICO = [
    	(DICO_PATH + '500-val.txt', '500-val'),
    	(DICO_PATH + '600-val.txt', '600-val'),
        #(DICO_PATH + '850-mots-us.txt', '850-mots'),
        #(DICO_PATH + '22600-mots-fr.txt', '22600-mots'),
        #(DICO_PATH + '58000-mots-us.txt', '58000-mots'),
        #(DICO_PATH + '133000-mots-us.txt', '133000-mots'),
        #(DICO_PATH + '135000-mots-fr.txt', '135000-mots')
    ]

    GRILLE = [
        (GRILLEVIDE_PATH + 'td3vide.mc', 'td3'),
        #(GRILLEVIDE_PATH + '11.mc', '11'),
        #(GRILLEVIDE_PATH + '12.mc', '12'),
        #(GRILLEVIDE_PATH + 'A.mc', 'A'),
        #(GRILLEVIDE_PATH + 'B.mc', 'B'),
        #(GRILLEVIDE_PATH + 'C.mc', 'C')
    ]

    ALGO = [
#        'AC3',
#        'CBJ',
#        'FC',
#        'CBJ_AC3',
#        'FC_AC3',
	'VAL'

    ]



    for gr in GRILLE:
        for al in ALGO:
            for dic in DICO:
                times = []
                print 'debut algo ' + str(al) + " " + str(dic[1]) + ' Grille :' + str(gr[1])
                for i in range(5):
                    dico = Dico(dic[0])
                    grille = Grille(gr[0])
                    grille.updateDico(dico)
                    algo = Algo(grille=grille, algoName=al, stat=True)
                    start = time.time()
                    algo.start()
                    algo.join(300)
                    elapse = time.time() - start
                    print 'fin ' + str(i+1) + ': ' + str(elapse)
                    times += [elapse]
                fichier = open(PATHSAVE+"temps_" + gr[1] + "_" + al + ".stat", "a")
                fichier.write(dic[1])
                moy = 0
                for  t in times:
                    fichier.write(" "+str(t))
                    moy += t
                print 'moyenne :' + str(moy/5)
                fichier.write("\n")
                fichier.close()


