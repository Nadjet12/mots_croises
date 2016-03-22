from copy import deepcopy

a = dict()
a['a'] = dict()
a['a']['a'] = 'aa'
a['a']['b'] = 'ab'
a['b'] = dict()
a['b']['a'] = 'ba'
a['b']['b'] = 'bb'

print 'a -> ' + str(a)

c = deepcopy(a)

print 'c -> ' + str(c)

a['a'] = 'ab'

print 'a -> ' + str(a)
print 'c -> ' + str(c)