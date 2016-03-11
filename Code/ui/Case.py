from Tkinter import Entry, StringVar


class Case(Entry):

    def __init__(self, *args, **kwargs):

        self.mot = kwargs.pop('m', None)
        self.ui = kwargs.pop('ui', None)
        self.pos = kwargs.pop('pos', None)
        Entry.__init__(self, *args, **kwargs)
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.char_callback(sv))
        self['textvariable'] = sv


    def char_callback(self,sv):
        #print "get " + sv.get()
        sv.set(sv.get().upper()[-1])

        s = "".join(sv.get())

        self.mot.set_lettre(self.pos, s)

    def setLettre(self, lettre):
        self.insert(0,lettre)
        pass