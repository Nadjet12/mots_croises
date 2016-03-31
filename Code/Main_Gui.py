#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import Tk

from gui.Gui import Gui


if __name__ == "__main__":
    root = Tk()
    root.resizable(width = True, height = True)
    interface = Gui(master=root)
    interface.master.title("RP : Mots Croisés (Bourdache Nadjet, Adequin Renaud)")
    interface.pack(fill="both", expand=True)
    interface.mainloop()
