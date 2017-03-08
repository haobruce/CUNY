from __future__ import division

def randGen(number, seed):
    currentVal = seed
    randoms = []
    a = 98723
    c = 192736
    m = 12731.0
    for i in range(1, number):
        currentVal = (a * currentVal + c) % m
        randoms.append(currentVal/m)
    print randoms

randGen(10, 234)
