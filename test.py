def func():
    b = range(18)
    a=[0,5,10,13,17]
    for i in xrange(0,len(a)-1):
        for j in xrange(a[i],a[i+1]):
            print b[j]

if __name__ == '__main__':
    func()
