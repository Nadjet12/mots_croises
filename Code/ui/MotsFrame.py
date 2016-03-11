#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkFont

from Case import Case
try:
    from Code.ui.UiMot import UiMot
except ImportError:
    import sys
    sys.path.append('./Code/ui/UiMot')

try:
    from tkinter import *
except ImportError:
    from Tkinter import *


class MotsFrame(Frame):

    def __init__(self, motFrame, grille=None, master=None):
        pass

    def set_Mots(self, listes):

        for l in listes:

            pass
