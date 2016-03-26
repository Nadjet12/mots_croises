import matplotlib.pyplot as plt


tab_algo = []
t = []
tab_nb = []

file = "./stat/temps_FC_AC3_C_24.stat"

fichier = open(file, "r")
i = 1
for line in fichier.readlines():
    l = line.split("\t")
    ll = l[0].split('-')
    tab_algo += [ll[0]+"\n " + ll[1]+ " " +ll[2]]
    tab_nb += [eval(l[1])]
    t += [i]
    i += 1

fig = plt.figure()
plt.suptitle("Temps Forward Checking avec AC3 Grille C")
ax = fig.add_subplot(111)

# Valeur a afficher
plt.plot(t, tab_nb, 'r--') # ligne rouge
plt.plot(t, tab_nb, 'b+') # points bleu
plt.xticks(t, tab_algo) # nom axe X

#limit en X et Y
ax.set_ylim(int(min(tab_nb)-1),int(max(tab_nb)+1))
ax.set_xlim([1,5])

# afficher la valeur
for i,j in zip(t,tab_nb):
    ax.annotate(str(round(j,3)),xy=(i,j))


plt.grid()
plt.show()