import sys
sys.path.insert(0, './ui')

import ToggledFrame as TogglF
import Tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()

    t = TogglF.ToggledFrame(root, text='Rotate', relief="raised", borderwidth=1)
    t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    tk.Label(t.sub_frame,  text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
    tk.Entry(t.sub_frame).pack(side="left")

    t2 = TogglF.ToggledFrame(root, text='Resize', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    for i in range(10):
        tk.Label(t2.sub_frame, text='Test' + str(i)).pack()

    t3 = TogglF.ToggledFrame(root, text='Fooo', relief="raised", borderwidth=1)
    t3.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")

    for i in range(10):
        tk.Label(t3.sub_frame, text='Bar' + str(i)).pack()

    root.mainloop()