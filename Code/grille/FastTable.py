import collections
import bisect
import random


class FastTable:

    def __init__(self):
        self.__deque = collections.deque()

    def __len__(self):
        return len(self.__deque)

    def head(self):
        return self.__deque.popleft()

    def tail(self):
        return self.__deque.pop()

    def peek(self):
        return self.__deque[-1]

    def insert(self, obj):
        index = bisect.bisect_left(self.__deque, obj)
        self.__deque.rotate(-index)
        self.__deque.appendleft(obj)
        self.__deque.rotate(index)


table = FastTable()

# (valeur, Noeud)
# 1er element du tuple la valeur et apres le Noeud
for k in range(random.randint(5, 10)):
    table.insert((random.random(), [random.randint(1, 10) for i in range(random.randint(1, 7))]))

table.insert((1, [random.randint(1, 10) for i in range(random.randint(1, 7))]))
table.insert((1, [random.randint(1, 10) for i in range(random.randint(1, 7))]))
table.insert((1, [random.randint(1, 10) for i in range(random.randint(1, 7))]))
table.insert((1, [random.randint(1, 10) for i in range(random.randint(1, 7))]))
print 'taille de la liste :' + str(len(table))



# liste de tout les max ==
maxtuple = table.tail()
maxval = maxtuple[0]
tmp = table.tail()

tableMax = [maxtuple]

while tmp[0] == maxval:
    tableMax += [tmp]
    tmp = table.tail()


print '\nelement non max a remettre dans la liste ' + str(tmp)
table.insert(tmp)



# la liste ne contient plus les max
print '\nelement restant\n'
while table:
    print "element :" + str(table.tail())


print "\nliste elements max :"

for i in tableMax:
    if i is tmp:
        print str(i) + "l'element est remis dans la liste :-)"
    else :
        print i