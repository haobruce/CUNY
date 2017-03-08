import timeit

setup = '''
import numpy as np

def sortwithloops(input):
    results = input[:]  # prevent overwriting input
    listlen = len(input)
    for i in range(1, listlen):
        for j in range(listlen - (listlen-1)):
            if input[i] < input[j]:
                input[i], input[j] = input[j], input[i]
    return results


def sortwithoutloops(input):
    results = input[:]
    return sorted(results)


def sortwithnumpy(input):
    results = np.array(input[:])
    return np.sort(results)


def listgen(n):
    return list(np.random.choice(xrange(100), n))
'''

if __name__ == '__main__':
    n = 1000
    t = timeit.Timer('l=listgen(10); sortwithloops(l)', setup=setup)
    print 'Sort using iteration (loops=%d, listlen=10)            : %f' % (n, t.timeit(n))
    t = timeit.Timer('l=listgen(10); sortwithoutloops(l)', setup=setup)
    print 'Sort using built-in python (loops=%d, listlen=10)      : %f' % (n, t.timeit(n))
    t = timeit.Timer('l=listgen(10); sortwithnumpy(l)', setup=setup)
    print 'Sort using numpy (loops=%d, listlen=10)                : %f' % (n, t.timeit(n))

    t = timeit.Timer('l=listgen(1000); sortwithloops(l)', setup=setup)
    print 'Sort using iteration (loops=%d, listlen=1000)          : %f' % (n, t.timeit(n))
    t = timeit.Timer('l=listgen(1000); sortwithoutloops(l)', setup=setup)
    print 'Sort using built-in python (loops=%d, listlen=1000)    : %f' % (n, t.timeit(n))
    t = timeit.Timer('l=listgen(1000); sortwithnumpy(l)', setup=setup)
    print 'Sort using numpy (loops=%d, listlen=1000)              : %f' % (n, t.timeit(n))

