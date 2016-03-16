import time
import re
from codecs import *

class Noeud:

    def __init__(self, peut_finir=False):
        self.peut_finir = peut_finir
        self.liste_Noeud = dict()

    def add_Fils(self, c, peut_finir):
        if c in self.liste_Noeud:
            self.liste_Noeud[c].setPeut_finir(peut_finir)
        else:
            self.liste_Noeud[c] = Noeud(peut_finir)
        return self.liste_Noeud[c]

    def getFils(self, c):
        if c in self.liste_Noeud:
            return self.liste_Noeud[c]
        return None

    def setPeut_finir(self, peut_finir):
        self.peut_finir |= peut_finir

    def get_list_Mots(self, pattern, mot, profondeur):
        liste = set()
        if profondeur == len(pattern)-1:
            if pattern[profondeur] in '.':
                for c, n in self.liste_Noeud.items():
                    if n.peut_finir:
                        liste.add(mot + c)
            else:
                if pattern[profondeur] in self.liste_Noeud and self.liste_Noeud[pattern[profondeur]].peut_finir:
                    liste.add(mot + pattern[profondeur])
        else:
            if pattern[profondeur] in '.':
                for c, n in self.liste_Noeud.items():
                    liste.update(n.get_list_Mots(pattern, mot+c, profondeur+1))
            else:
                if pattern[profondeur] in self.liste_Noeud:
                    liste.update(self.liste_Noeud[pattern[profondeur]].get_list_Mots(pattern, mot+pattern[profondeur], profondeur+1))
        return liste

    def update(self, pattern, mot, profondeur):
        if profondeur == len(pattern)-1:
            if pattern[profondeur] in '.':
                return
            else:
                if pattern[profondeur] in self.liste_Noeud:
                    d = dict()
                    d[0] = self.liste_Noeud[pattern[profondeur]]
                    self.liste_Noeud = d
        else:
            if pattern[profondeur] in '.':
                for c, n in self.liste_Noeud.items():
                    n.update(pattern, mot+c, profondeur+1)
            else:
                if pattern[profondeur] in self.liste_Noeud:
                    d = dict()
                    d[pattern[profondeur]] = self.liste_Noeud[pattern[profondeur]]
                    self.liste_Noeud = d
                    print pattern[profondeur]
                    print mot
                    self.liste_Noeud[pattern[profondeur]].update(pattern, mot+pattern[profondeur], profondeur+1)

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
                if self.getFils(c):
                    d[c] = self.getFils(c)
            self.liste_Noeud = d
            b = len(listes) != len(self.liste_Noeud)
            return b
        else:
            for c, n in self.liste_Noeud.items():
                return n.updateFromContraintes(profondeur-1, listes)



class Dico:
    def __init__(self, file=None, liste=None):
        self.lettres = dict()
        lines = None
        if file:
            lines = open(file, encoding="ISO-8859-1").readlines()
        elif liste:
            lines = liste

        for line in lines:
            line = line.rstrip()
            self.add_Mot(line)

    def add_Mot(self, mot):
        mot = mot.upper()
        n  = self.get_Lettre(mot[0])
        for l in mot[1:]:
            n = n.add_Fils(l, False)
        n.setPeut_finir(True)

    def get_Lettre(self, c, peut_finir=False):
        if c in self.lettres:
            return self.lettres[c]
        self.lettres[c] = Noeud(peut_finir)
        return self.lettres[c]

    def get_New_Domaine(self, mot_Imcomplet):
        mot_Imcomplet = mot_Imcomplet.upper()
        liste = set()
        if (mot_Imcomplet[0] in '.'):
            for c, n in self.lettres.items():
                liste.update(n.get_list_Mots(mot_Imcomplet, c, 1))
        else:
            if mot_Imcomplet[0] in self.lettres:
                liste.update(self.lettres[mot_Imcomplet[0]].get_list_Mots(mot_Imcomplet, mot_Imcomplet[0], 1))
        return liste

    def update(self, pattern):
        pattern = pattern.upper()
        if pattern[0] in '.':
            for c, n in self.lettres.items():
                n.update(pattern, c, 1)
        else:
            if pattern[0] in self.lettres:
                d = dict()
                d[0] = self.lettres[pattern[0]]
                self.lettres = d
                self.lettres[pattern[0]].update(pattern, [pattern[0]],1)

    def get_Domaine(self, taille):
        return self.get_New_Domaine(''.join(['.' for i in range(taille)]))

    def getAllLettre(self,profondeur):
        lettres = set()
        profondeur -= 1
        if profondeur == 0:
            for c, n in self.lettres.items():
                    lettres.add(c)
            return lettres

        else:

            for c, n in self.lettres.items():
                lettres.union(n.getAllLetter(lettres, profondeur-1))
            return lettres

    def updateFromContraintes(self,profondeur, listes):
        profondeur -= 1
        if profondeur == 0:
            d = dict()
            b = False
            for c in listes:
                if self.get_Lettre(c):
                    d[c] = self.get_Lettre(c)
            b = len(listes) != len(self.lettres)
            return b
        else:
            for c, n in self.lettres.items():
                return n.updateFromContraintes(profondeur-1, listes)


file = ["abcd", "abce","abff", "abfg"]
#
#start_time = time.time()
#
d = Dico(liste=file)
print d.get_Domaine(4)
print 'all : ' + str(d.getAllLettre(4))
#d.update('..C.')
print d.get_Domaine(4)
print 'all : ' + str(d.updateFromContraintes(3, 'c'))
print d.get_Domaine(4)
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
#start_time = time.time()
#string = ' '.join([line.rstrip() for line in open(file, encoding="ISO-8859-1")])+' '
#elapsed_time = time.time() - start_time
#res = re.findall(pattern, string)
#print("recherche mot \"" + pattern + "\" regex " + str(len(res)) + " : " + str(elapsed_time))
#print(res)
#print()
