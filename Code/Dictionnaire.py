import time
import re

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
        return self.liste_Noeud[c]

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


class Dico:
    def __init__(self, file):
        self.lettres = dict()
        lines = open(file, encoding="ISO-8859-1").readlines()
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

    def get_Domaine(self, taille):
        return self.get_New_Domaine(''.join(['.' for i in range(taille)]))



file = "./mots/135000-mots-fr.txt"

start_time = time.time()

d = Dico(file)
elapsed_time = time.time() - start_time
print("creation dictionnaire " + file + " : " + str(elapsed_time))
print()


taille = 15
start_time = time.time()
res = d.get_Domaine(taille)

elapsed_time = time.time() - start_time
print("recherche taille "+ str(taille) + " dictionnaire " + str(len(res)) + " : " + str(elapsed_time))
print()

pattern = "....k"
start_time = time.time()
res = d.get_New_Domaine(pattern)
elapsed_time = time.time() - start_time
print("recherche mot \"" + pattern + "\" dictionnaire " + str(len(res)) + " : " + str(elapsed_time))
print(res)
print()


pattern = " "+pattern+" "
pattern = pattern.replace('.', '\w')
string = ' '.join([line.rstrip() for line in open(file, encoding="ISO-8859-1")])+' '
start_time = time.time()
p = re.compile(pattern)
res = p.findall(string)
elapsed_time = time.time() - start_time
print("recherche mot \"" + pattern + "\" regex " + str(len(res)) + " : " + str(elapsed_time))
print(res)
print()

pattern = " stock "
start_time = time.time()
string = ' '.join([line.rstrip() for line in open(file, encoding="ISO-8859-1")])+' '
elapsed_time = time.time() - start_time
res = re.findall(pattern, string)
print("recherche mot \"" + pattern + "\" regex " + str(len(res)) + " : " + str(elapsed_time))
print(res)
print()
