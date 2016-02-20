from Code.ui import ToggledFrame as TogglF
import tkinter

if __name__ == "__main__":
    root = tkinter.Tk()

    t = TogglF.ToggledFrame(root, text='Rotate', relief="raised", borderwidth=1)
    t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    tkinter.Label(t.sub_frame,  text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
    tkinter.Entry(t.sub_frame).pack(side="left")

    t2 = TogglF.ToggledFrame(root, text='Resize', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    for i in range(10):
        tkinter.Label(t2.sub_frame, text='Test' + str(i)).pack()

    t3 = TogglF.ToggledFrame(root, text='Fooo', relief="raised", borderwidth=1)
    t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    for i in range(10):
        tkinter.Label(t3.sub_frame, text='Bar' + str(i)).pack()

    root.mainloop()