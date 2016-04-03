# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
BEGIN = 'temps_'
END = '.stat'
PATHSAVE = '../Stat/stat/'
FILE = [
#    (BEGIN + 'A_AC3' + END, 'A', 'Arc-consistance'),
#    (BEGIN + 'B_AC3' + END, 'B', 'Arc-consistance'),
#    (BEGIN + 'C_AC3' + END, 'C', 'Arc-consistance'),
#    (BEGIN + '7_AC3' + END, '7', 'Arc-consistance'),

    (BEGIN + 'A_CBJ' + END, 'A', 'CBJ'),
#     (BEGIN + 'B_CBJ' + END, 'B', 'CBJ'),
#    (BEGIN + 'C_CBJ' + END, 'C', 'CBJ'),
#    (BEGIN + '7_CBJ' + END, '7', 'CBJ'),

    (BEGIN + 'A_CBJ_AC3' + END, 'A', 'CBJ avec Arc-consistance'),
#     (BEGIN + 'B_CBJ_AC3' + END, 'B', 'CBJ avec Arc-consistance'),
#    (BEGIN + 'C_CBJ_AC3' + END, 'C', 'CBJ avec Arc-consistance'),
#    (BEGIN + '7_CBJ_AC3' + END, '7', 'CBJ avec Arc-consistance'),

    (BEGIN + 'A_FC' + END, 'A', 'FC'),
#     (BEGIN + 'B_FC' + END, 'B', 'FC'),
#    (BEGIN + 'C_FC' + END, 'C', 'FC'),
#    (BEGIN + '7_FC' + END, '7', 'FC'),

    (BEGIN + 'A_FC_AC3' + END, 'A', 'FC avec Arc-consistance'),
#     (BEGIN + 'B_FC_AC3' + END, 'B', 'FC avec Arc-consistance'),
#    (BEGIN + 'C_FC_AC3' + END, 'C', 'FC avec Arc-consistance'),
#    (BEGIN + '7_FC_AC3' + END, '7', 'FC avec Arc-consistance'),
]

fig = plt.figure()
plt.suptitle("Temps de resolution " + " sur la grille A")
ax = fig.add_subplot(111)
mini = 0
maxi = 0
couleur = [['r','m','g', 'b'], ['r','m','g', 'b']]
c = 0
for f in FILE:
    file = f[0]
    grille = f[1]
    algo = f[2]
    t = []

    fichier = open(PATHSAVE+file, "r")
    nomdico = []
    res = [[], [], [], [], [], [], []]

    i = 1
    for line in fichier.readlines():
        sline = line.split(' ')
        nomdico += [sline[0]]
        tmp  = (float(eval(sline[1])) + float(eval(sline[2])) + float(eval(sline[3])) + float(eval(sline[4])) + float(eval(sline[5])))/5.0
        res[0] += [float(eval(sline[1]))]
        res[1] += [float(eval(sline[2]))]
        res[2] += [float(eval(sline[3]))]
        res[3] += [float(eval(sline[4]))]
        res[4] += [float(eval(sline[5]))]
        res[5] += [float(eval(sline[5]))]
        res[6] += [tmp]
        t += [i]
        i+=1
        mini = min(mini, int(eval(sline[1])), int(eval(sline[2])), int(eval(sline[3])), int(eval(sline[4])), int(eval(sline[5])))
        maxi = max(maxi, int(eval(sline[1])), int(eval(sline[2])), int(eval(sline[3])), int(eval(sline[4])), int(eval(sline[5])))

    plt.scatter(t, res[0], s=100, c=couleur[0][c], marker=".")
    for tab in res[1:]:
        plt.scatter(t, tab, s=100, c=couleur[0][c], marker=".")
    plt.plot(t, res[6], couleur[1][c]+'-', label=algo) # points bleu
    for i,j in zip(t,res[6]):
        ax.annotate(str(round(j,3)),xy=(i,j))

    plt.xticks(t, nomdico) # nom axe X
    c+=1
plt.legend(loc='upper left')
ax.set_ylim(max(mini-1, 0) , maxi +1 )
ax.set_xlim([0,6])
plt.grid()
plt.show()