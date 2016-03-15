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

    def add_ui(self, ui):
        self.guis += ui

    def char_callback(self, sv):
        c = sv.get()
        if c is'':
            for u in self.guis:
                u[0].update()
            return
        c = c.upper()
        c = c[-1]
        sv.set(c)

        s = "".join(c)
        for u in self.guis:
                u[0].update()
                u[2].set_lettre(u[1], s)

    def setLettre(self, lettre):
        if lettre is ' ':
            return
        self.delete(0, 'end')
        self.insert(0, lettre)