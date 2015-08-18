__author__ = 'tangyh'

def split(basepath, srcfile, trgfile, trainport, validport):
    source = open(basepath+srcfile, 'rb').readlines()
    target = open(basepath+trgfile, 'rb').readlines()
    assert len(source)==len(target), 'sentence should be equal size'
    totalsents=len(source)

    trainsrc=open(basepath+'trainsrc', 'wb')
    traintrg=open(basepath+'traintrg', 'wb')
    validsrc=open(basepath+'validsrc', 'wb')
    validtrg=open(basepath+'validtrg', 'wb')
    testsrc=open(basepath+'testsrc', 'wb')
    testtrg=open(basepath+'testsrc', 'wb')

    traincnt = xrange(int(totalsents*trainport))
    validcnt = xrange(int(totalsents*trainport), int(totalsents*(trainport+validport)))
    testcnt = xrange(int(totalsents*(trainport+validport)), totalsents)

    for i in traincnt:
        trainsrc.write(source[i])
        traintrg.write(target[i])

    for i in validcnt:
        validsrc.write(source[i])
        validtrg.write(target[i])

    for i in testcnt:
        testsrc.write(source[i])
        testtrg.write(target[i])

    trainsrc.close()
    traintrg.close()
    validsrc.close()
    validtrg.close()
    testsrc.close()
    testtrg.close()

if __name__ == "__main__":
    basepath = '/home/tangyaohua/dl4mt/data/large.corpus'
    srcfile = 'english'
    trgfile = 'chinese'
    split(basepath, srcfile, trgfile, 0.8, 0.1)