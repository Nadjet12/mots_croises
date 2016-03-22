# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:22:49 2016

@author: 3501796
"""

class Noeud:

    def __init__(self, pere, motListe, motObj, couple):
        self.pere = pere
        self.fils = []
        self.listeMot = motListe
        self.motObj = motObj
        self.mot = couple[0]
        self.value = couple[1]
        
    
    def update_Peres(self):
        '''
        la valeur d'un noeud est le 
        MIN entre sa valeur et le max de ses fils
        
        Si la valeur du Noeud a changé alors on met a jour le pere 
        '''
        
        # le premier élément est le plus grand
        sorted(self.fils, key=lambda value: (value[1]), reverse=True)
        
        val = min(self.value, self.listeMot[0][0])
        
        if self.value != val:
            self.value = val
            self.pere.update_Peres()
        
        
    def create_Fils(self):
        if not self.listeMot:
            # si la liste est vide ce noeud est la meilleur solution            
            return 
            
        m = self.motListe[0]
        for mot in m.getDomaine():
            self.fils += [Noeud(self, self.motListe[1:], m, mot[0], mot[1])]
        
        # tri la liste en fonction de la valeur du second argument du plus grand au plus petit        
        sorted(self.fils, key=lambda value: (value[1]), reverse=True)
        

class Arbre:
    
    def __init__(self, mot, motListe):
        self.listeNoeud = []
        for el in mot.getDomaine():
            self.listeNoeud += [Noeud(None, motListe, mot, el)]
        sorted(self.listeNoeud, key=lambda value: (value[1]), reverse=True)
        
    
    def get_Noeud_Max(self):
        sorted(self.listeNoeud, key=lambda value: (value[1]), reverse=True)
        return self.listeNoeud[0]
        
        
    
    