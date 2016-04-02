import matplotlib.pyplot as plt
BEGIN = 'temps_'
END = '.stat'
FILE = [
#    (BEGIN + 'A_AC3' + END, 'A', 'Arc-consistance'),
#    (BEGIN + 'B_AC3' + END, 'B', 'Arc-consistance'),
#    (BEGIN + 'C_AC3' + END, 'C', 'Arc-consistance'),
#    (BEGIN + '7_AC3' + END, '7', 'Arc-consistance'),

#    (BEGIN + 'A_CBJ' + END, 'A', 'Conflict BackJumping'),
#    (BEGIN + 'B_CBJ' + END, 'B', 'Conflict BackJumping'),
    (BEGIN + 'C_CBJ' + END, 'C', 'Conflict BackJumping'),
#    (BEGIN + '7_CBJ' + END, '7', 'Conflict BackJumping'),

#    (BEGIN + 'A_FC' + END, 'A', 'Forward Checking'),
#    (BEGIN + 'B_FC' + END, 'B', 'Forward Checking'),
    (BEGIN + 'C_FC' + END, 'C', 'Forward Checking'),
#    (BEGIN + '7_FC' + END, '7', 'Forward Checking'),

#    (BEGIN + 'A_FC_AC3' + END, 'A', 'Forward Checking avec Arc-consistance'),
#    (BEGIN + 'B_FC_AC3' + END, 'B', 'Forward Checking avec Arc-consistance'),
    (BEGIN + 'C_FC_AC3' + END, 'C', 'Forward Checking avec Arc-consistance'),
#    (BEGIN + '7_FC_AC3' + END, '7', 'Forward Checking avec Arc-consistance'),
]

for f in FILE:
    file = f[0]
    grille = f[1]
    algo = f[2]
    t = []

    fichier = open('./'+file, "r")
    nomdico = []
    res = [[], [], [], [], [], []]
    mini = 0
    maxi = 0
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
        res[5] += [tmp]
        t += [i]
        i+=1
        mini = min(mini, int(eval(sline[1])), int(eval(sline[2])), int(eval(sline[3])), int(eval(sline[4])), int(eval(sline[5])))
        maxi = max(maxi, int(eval(sline[1])), int(eval(sline[2])), int(eval(sline[3])), int(eval(sline[4])), int(eval(sline[5])))
    fig = plt.figure()
    plt.suptitle("Temps " + algo + " sur la grille " + grille)
    ax = fig.add_subplot(111)
    plt.scatter(t, res[0], s=100, c='b', marker=".", label='valeurs')
    for tab in res[1:]:
        plt.scatter(t, tab, s=100, c='b', marker=".")
    plt.plot(t, res[5], 'r--', label='moyenne') # points bleu
    for i,j in zip(t,res[5]):
        ax.annotate(str(round(j,3)),xy=(i,j))
    plt.legend(loc='upper left')
    ax.set_ylim(max(mini-1, 0) , maxi +1 )
    ax.set_xlim([0,6])
    plt.xticks(t, nomdico) # nom axe X
    plt.grid()
    plt.show()