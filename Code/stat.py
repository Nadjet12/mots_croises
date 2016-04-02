import time
from grille.Grille import Grille

from grille.Dictionnaire import Dico

from grille.Algos import Algo

DICO_PATH = '../Data/mots/'
GRILLEVIDE_PATH = '../Data/grillesVides/'
if __name__ == "__main__":

    DICO = [
        (DICO_PATH + '850-mots-us.txt', '850-mots'),
        (DICO_PATH + '22600-mots-fr.txt', '22600-mots'),
        (DICO_PATH + '58000-mots-us.txt', '58000-mots'),
        (DICO_PATH + '133000-mots-us.txt', '133000-mots'),
        (DICO_PATH + '135000-mots-fr.txt', '135000-mots')
    ]

    GRILLE = [
        (GRILLEVIDE_PATH + 'A.mc', 'A'),
        (GRILLEVIDE_PATH + 'B.mc', 'B'),
        (GRILLEVIDE_PATH + 'C.mc', 'C'),
        (GRILLEVIDE_PATH + '7.mc', '7')
    ]

    ALGO = [
        'AC3',
        'FC',
        'FC_AC3',
        'CBJ'
    ]





    for al in ALGO:
        for dic in DICO:
            times = []
            print 'debut algo ' + str(al) + " " + str(dic[1])
            for i in range(5):
                dico = Dico(dic[0])
                grille = Grille(GRILLE[1][0])
                grille.updateDico(dico)
                algo = Algo(grille=grille, algoName=al)
                start = time.time()
                algo.start()

                algo.join()
                elapse = time.time() - start
                print 'fin ' + str(i+1) + ': ' + str(elapse)
                times += [elapse]

            fichier = open("./temps_"+al+"_"+GRILLE[1][1]+".stat", "a")
            fichier.write(dic[1])
            for  t in times:
                fichier.write(" "+str(t))
            fichier.write("\n")
            fichier.close()


