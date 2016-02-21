#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from tkinter import *
except ImportError:
    from Tkinter import *


class MainFrame(Frame):

    def __init__(self, master=None):

        Frame.__init__(self, master)
        
        self.frameGrille = None
        self.grille = None
        self.frameMot = None
        
        
        menubar = Menu(master)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)

        newGameMenu = Menu(menubar, tearoff=0)
        filemenu.add_cascade(label="Nouvelle partie", menu=newGameMenu)
        vsia = Menu(newGameMenu, tearoff=0)
        newGameMenu.add_cascade(label="Vs IA", menu=vsia)
        vsia.add_command(label="Min/Max", command=None)
        newGameMenu.add_command(label="2 Joueurs", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=master.quit)
       
       
        menubar.add_cascade(label="Fichier", menu=filemenu)


        master.config(menu=menubar)
        
        
if __name__ == "__main__":
    root = Tk()

    interface = MainFrame(master=root)
    interface.master.title("AWÉLÉ")

    interface.pack(fill="both", expand=True)

    interface.mainloop()