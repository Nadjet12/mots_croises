import random
import time
import re
from codecs import *

class Noeud:

    def __init__(self, peut_finir=False, value=0):
        self.peut_finir = peut_finir
        self.liste_Noeud = dict()
        self.value = value

    def add_Fils(self, c, peut_finir, value=0):
        if c in self.liste_Noeud:
            self.liste_Noeud[c].setPeut_finir(peut_finir)
        else:
            self.liste_Noeud[c] = Noeud(peut_finir)
        return self.liste_Noeud[c]

    def getFils(self, c):
        return self.liste_Noeud[c]

    def setPeut_finir(self, peut_finir, value=0):
        self.peut_finir |= peut_finir
        self.value = value

    def get_list_Mots(self, pattern, mot, profondeur, getValue=False):
        liste = set()
        if profondeur == len(pattern)-1:
            if pattern[profondeur] in '.':
                for c, n in self.liste_Noeud.items():
                    if n.peut_finir:
                        if getValue:
                            liste.add((mot + c, n.value))
                        else:
                            liste.add(mot + c)
            else:
                if pattern[profondeur] in self.liste_Noeud and self.liste_Noeud[pattern[profondeur]].peut_finir:
                    print self.value
                    if getValue:
                        liste.add((mot + pattern[profondeur], self.liste_Noeud[pattern[profondeur]].value))
                    else:
                        liste.add(mot + pattern[profondeur])

        else:
            if pattern[profondeur] in '.':
                for c, n in self.liste_Noeud.items():
                    liste.update(n.get_list_Mots(pattern, mot+c, profondeur+1, getValue))
            else:
                if pattern[profondeur] in self.liste_Noeud:
                    liste.update(self.liste_Noeud[pattern[profondeur]].get_list_Mots(pattern, mot+pattern[profondeur], profondeur+1, getValue))
        return liste

    def getAllLetter(self,lettres, profondeur):
        if profondeur == 0:
            for c, n in self.liste_Noeud.items():
                    lettres.add(c)
            return lettres
        else:
            for c, n in self.liste_Noeud.items():
                lettres.union(n.getAllLetter(lettres, profondeur-1))
            return lettres

    def updateFromContraintes(self,profondeur, listes):
        if profondeur == 0:
            d = dict()
            for c in listes:
                if c in self.liste_Noeud:
                    d[c] =self.liste_Noeud[c]
            b = len(d) != len(self.liste_Noeud)
            self.liste_Noeud = d
            return b
        else:
            bool = False
            for c, n in self.liste_Noeud.items():
                bool |= n.updateFromContraintes(profondeur-1, listes)
            return bool

    def removeMot(self, mot):
        mot = mot.upper()
        if len(mot) == 1:
            self.liste_Noeud[mot[0]].peut_finir= False
        else:
            self.liste_Noeud[mot[0]].removeMot(mot[1:])


class Dico:

    def __init__(self, file=None, liste=None, value=False):
        self.lettres = dict()
        lines = None
        if file:
            lines = open(file, encoding="ISO-8859-1").readlines()
        elif liste:
            lines = liste
        for line in lines:
            #line = line.decode('ISO-8859-1').encode('utf8')
            line = line.rstrip()
            line = line.split(' ')
            v = random.random()
            if len(line)> 1:
                v = eval(line[1])

            self.add_Mot(line[0], value=v)

    def add_Mot(self, mot, value=0):
        print value
        mot = mot.upper()
        n  = self.get_Lettre(mot[0])
        for l in mot[1:]:
            n = n.add_Fils(l, False)
        n.setPeut_finir(True, value)

    def get_Lettre(self, c, peut_finir=False):
        if c in self.lettres:
            return self.lettres[c]
        self.lettres[c] = Noeud(peut_finir)
        return self.lettres[c]

    def get_New_Domaine(self, mot_Imcomplet, getValue=False):
        mot_Imcomplet = mot_Imcomplet.upper()
        liste = set()
        if (mot_Imcomplet[0] in '.'):
            for c, n in self.lettres.items():
                liste.update(n.get_list_Mots(mot_Imcomplet, c, 1, getValue))
        else:
            if mot_Imcomplet[0] in self.lettres:
                liste.update(self.lettres[mot_Imcomplet[0]].get_list_Mots(mot_Imcomplet, mot_Imcomplet[0], 1, getValue))
        return liste

    def removeMot(self, mot):
        mot = mot.upper()
        if len(mot) == 1:
            self.lettres[mot[0]].peut_finir= False
        else:
            self.lettres[mot[0]].removeMot(mot[1:])

    def get_Domaine(self, taille, getValue=False):
        return self.get_New_Domaine(''.join(['.' for i in range(taille)]), getValue)

    def getAllLettre(self,profondeur):
        lettres = set()
        #profondeur -= 1
        if profondeur == 0:
            for c, n in self.lettres.items():
                    lettres.add(c)
            return lettres
        else:
            for c, n in self.lettres.items():
                lettres.union(n.getAllLetter(lettres, profondeur-1))
            return lettres

    def updateFromContraintes(self, profondeur, listes):
        #profondeur -= 1
        if profondeur == 0:
            d = dict()
            for c in listes:
                if c in self.lettres:
                    d[c] = self.lettres[c]
            b = len(d) != len(self.lettres)
            self.lettres = d
            return b
        else:
            bool = False
            for c, n in self.lettres.items():
                bool |= n.updateFromContraintes(profondeur-1, listes)
            return bool

if __name__ == "__main__":
    file = ["abca 1", "acbe","abcb 1", "fbfc"]
    #
    #start_time = time.time()
    #
    d = Dico(liste=file)
    print d.get_Domaine(4, getValue=True)
    print d.getAllLettre(3)
    d.updateFromContraintes(3, ["B", "C"])
    print d.getAllLettre(3)
    print d.get_Domaine(4, getValue=True)
    #elapsed_time = time.time() - start_time
    #print("creation dictionnaire " + file + " : " + str(elapsed_time))
    #print ""
    #
    #
    #taille = 15
    #start_time = time.time()
    #res = d.get_Domaine(taille)
    #
    #elapsed_time = time.time() - start_time
    #print("recherche taille "+ str(taille) + " dictionnaire " + str(len(res)) + " : " + str(elapsed_time))
    #print()
    #
    #pattern = "....k"
    #start_time = time.time()
    #res = d.get_New_Domaine(pattern)
    #elapsed_time = time.time() - start_time
    #print("recherche mot \"" + pattern + "\" dictionnaire " + str(len(res)) + " : " + str(elapsed_time))
    #print(res)
    #print()
    #
    #
    #pattern = " "+pattern+" "
    #pattern = pattern.replace('.', '[a-zA-Z]')
    #string = ' '.join([line.rstrip() for line in open(file, encoding="ISO-8859-1")])+' '
    #start_time = time.time()
    #p = re.compile(pattern)
    #res = p.findall(string)
    #elapsed_time = time.time() - start_time
    #print("recherche mot \"" + pattern + "\" regex " + str(len(res)) + " : " + str(elapsed_time))
    #print(res)
    #print()
    #
    #pattern = " stock "
    #sta    rt_time = time.time()
    #string = ' '.join([line.rstrip() for line in open(file, encoding="ISO-8859-1")])+' '
    #elapsed_time = time.time() - start_time
    #res = re.findall(pattern, string)
    #print("recherche mot \"" + pattern + "\" regex " + str(len(res)) + " : " + str(elapsed_time))
    #print(res)
#pri    nt()
