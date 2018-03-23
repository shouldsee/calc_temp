import random
import numpy as np

def gen_randwalk(ini,clen=10000):
    if isinstance(ini,np.ndarray):
        ini = ini.tolist()
    curr = ini
    it = iter([])
    while True:
        yield curr
        i = next(it,None)
        if i is None:
            idx = np.random.randint(102,size=(clen,))
            it=iter(idx)
            i = next(it)
        curr[i]=1-curr[i]
it = gen_randwalk(np.random.randint(2,size=(102,)))
for i,e in enumerate(it):
    print e
    if i == 10:
        break
        
def gen_longbin(part = [10]*10+[2]):
    rds0 = [range(2**i) for i in part]
    rds = [x[:] for x in rds0]
    map(random.shuffle,rds)
    
    fmt = ''.join(['{:0%db}'%n for n in part])
    for e in itertools.product(*rds0):
        decs = [r[x] for r,x in zip(rds,e)]
        yield fmt.format(*decs)
# rds = copy.deepcopy(rds0)
it = gen_longbin([10]*10+[2])

for i,e in enumerate(it):
    print e
    if i == 10:
        break