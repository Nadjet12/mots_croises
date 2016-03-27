from Tkinter import Entry, StringVar


class Case(Entry):

    def __init__(self, *args, **kwargs):

        self.guis = []
        ui = kwargs.pop('ui', None)
        if ui:
            self.guis += [(ui, kwargs.pop('pos', None), kwargs.pop('m', None))]
        Entry.__init__(self, *args, **kwargs)
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.char_callback(sv))
        self['textvariable'] = sv
        self.bind("<FocusIn>", self.focusCase)
        self.bind("<FocusOut>", self.unfocusCase)



    def add_ui(self, ui):
        self.guis += ui
        self.guis = list(set(self.guis))

    def char_callback(self, sv):
        if sv.get() is "":
            return
        c = sv.get()[-1]
        c = c.upper()
        sv.set(c)
        for u in self.guis:
            u[2].set_lettre(u[1], c, u[2])
            u[0].update(self)


    def setLettre(self, lettre):
        if lettre is ' ':
            return
        self.delete(0, 'end')
        self.insert(0, lettre)

    def focusCase(self, event):
        for u in self.guis:
            u[0].focusMot(self)

    def unfocusCase(self, event):
        for u in self.guis:
            u[0].unfocusMot()



    def setFocus(self, case=False):
        if case:
            self['bg'] = 'orange'
        else :
            self['bg'] = 'yellow'

    def setUnfocus(self):
        self['bg'] = 'white'
