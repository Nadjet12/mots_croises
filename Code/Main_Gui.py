#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import Tk

from ui.MainFrame import MainFrame

if __name__ == "__main__":
    root = Tk()

    interface = MainFrame(master=root)
    interface.master.title("Mots Croisés")
    # interface.master.geometry('{}x{}'.format(800, 600))
    interface.pack(fill="both", expand=True)

    interface.mainloop()
