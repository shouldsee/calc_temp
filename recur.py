from KBs import *
def get_parent_shape(avc,t):
    spdim = avc.shape[1:]
    pardim = list(x+t*2 for x in spdim)
    if spdim[-1] == 1:
        pardim[-1] = 1
#     pardim =tuple(x+t*2 if x!=1 else x for x in spdim)
    return tuple(pardim)

def findparent(avc,env,t=1,method='brute'):
    pardim = get_parent_shape(avc,t)
    nbit = np.prod(pardim)
    parent = itertools.product(*[range(2)]*nbit)
#     print len(list(parent))
    parent = np.reshape(list(parent),(2**nbit,)+pardim)
#     print parent.shape
    
    out = sample(env, ini = parent,T = t)
    bot = out[-1]
    
    realdim = [i for i,x in enumerate(bot.shape) if x!=1 and i!=0]
    for ax in realdim:
        bot= np.take(bot,range(t,bot.shape[ax]-t),axis=ax)
    res  = bot[:,None]
    targ = avc[None]
    graph = np.all(res == targ,axis=(-1,-2))
    return parent,graph

def glider2num(glider):
    ini = np.reshape(map(int,glider),(1,-1,1))
    fir = np.reshape(2**np.arange(ini.size),(1,-1,1))
    ini_int = convolve_int(ini,fir,'reflect').flat[(ini.size-1)//2]
    return ini_int

def main(env,glider,particle=None,per = 2,T=5,silent=1,findall=0):
    outlst = []
    if particle is None:
        particle = glider2num(glider)
    ini = np.reshape(map(int,glider),(1,-1,1))
    fir = np.reshape(2**np.arange(ini.size),(1,-1,1))
#     fir = np.reshape(2**np.arange(ini.size),(1,-1,1))
#     ini_int = convolve_int(ini,fir,'reflect').flat[(ini.size-1)//2]

    out = sample(env,ini=ini,)
#     showsptime(np.squeeze(out).T)
#     plt.show()

#     T = 7
    out = -.1*np.ones( get_parent_shape(ini,T) + (1+T,),dtype=np.float)
    # raise Exception()
    for t in range(0,T+1):
        if t ==0:
            parent = ini
            paridx = 0
        else:
            parent,paridx = findparent(ini,env,t = t)
        validPar = parent[np.ravel(paridx)]
        recur = convolve_int(validPar,fir,'wrap') == particle

        if per:
            move = cmp(per,0)*(t//abs(per))
#             print move
        else:
            move = 0
#         driftidx=  t + move + (parent[0].size-1)//2
        driftidx=  t + move + (+ini.size-1)//2
        obsidx = recur[:, driftidx]    
        if not silent:
            print recur.shape
            print np.shape(obsidx)
            print obsidx.mean()
        if findall:
            outlst.append(validPar)
        else:
            outlst.append(validPar[obsidx.ravel()])
        row = np.mean(recur,axis=0)
        idx = range(T-t,T-t+len(row))
    #     out
    #     print row.shape
        if t==0:
            row = ini
        out[idx,:,t] = row
    #     break
    if not silent:
        showsptime(out.T)
        plt.show()
    res = outlst
#     print [np.shape(x) for x in res]
    tiles = [ {'parity':{'T':T,'per':per},
       'seq':tuple(sum(x,[]) ),} for x in np.array(res[T]).tolist()]        
    return tiles





# n = 1

from simpleCycles import simple_cycles
def adj2dct(adj):
    idx = np.where(adj)
    g = {x:[] for x in range(len(adj))}
    for I,O in np.transpose(idx):
        g[I] = g.get(I,[]) + [O]
    return g


def tile_flatten(x):
    def f(x):
        return (x['parity']['T'],x['parity']['per'],) + tuple(x['seq'])
    if isinstance(x,list):
        return map(f,x)
    else:
        return f(x)
#     tiles = [ (x['parity']['T'],x['partiy']['per'],) + tuple(x['seq']) for x in tdct]
#     return tiles
def par2tiles(env,T,per,n=1,flat=0):
#     T = 3
#     per =  2
    lst = [base2bin(str(x),10,n) for x in range(2**n)]
#     res = map(lambda x:main(x,per=per,T=T),lst);
    tiles = map(lambda x:main(env,x,per=per,T=T),lst);
    # tiles = np.vstack([x[T] for x in res])
    tiles = sum(tiles,[])
#     tiles = [ {'parity':{'T':T,'per':per},
#        'seq':tuple(x),} for x in np.squeeze(np.vstack(x[T] for x in res)).tolist()]
    if flat:
        tiles = map(tile_flatten,tiles)
#     tiles = [ (T,per,) + tuple(x) for x in np.squeeze(np.vstack(x[T] for x in res)).tolist()]
    return tiles 
# tile0 = par2tiles(2,0)


def safe_divide(T,per):
    if per:
        return T/per
    else:
        return 0


def isCompatible(left,right,T = 1,n =  1):
#     lPar =left.get('parity')
#     rPar =right.get('parity')    
    
    #### Currently assuming the T are the same    
    
    ##### Assuming both are of per 0
    #### Tail of left matches Head of right
#     tail = left['seq'][-2*lPar['T']:]
#     head = right['seq'][:2*rPar['T']]
    lper = left[1] 
    rper = right[1]
    ldri = safe_divide(T,lper)
    rdri = safe_divide(T,rper)
    jumplen = ldri - rdri
    assert 2*T-jumplen>=0,'Negative overlap due to huge jump'
        
#     tail = left [-(2*T-jumplen)  :     ]     ### len = 2*T - jumplen
#     head = right[2  : 2 + (2*T- jumplen)] ### len = 2*T - jummplen
    tail = left [2+n:   ]     ### len = 2*T - n
    head = right[2  : -n]        ### len = 2*T - n
    tailtail = tail[jumplen:]
    headhead = head[:-jumplen] if jumplen>0 else head
    if all(x==y for x,y in zip(headhead,tailtail)):
        consent =  headhead
        if  jumplen>0:
            jumphist = np.hstack([tail[:jumplen],head])
#             jumphist = tuple(tail[:jumplen]) + tuple(head)
            end = sample(env, ini =np.reshape(jumphist,(1,-1,1)),T=T)[-1]
            end = end.ravel()[T:-T]
            print jumphist,end
            return 0.5
        else:
    #         print head,tail
            return True
    else:
        return False

def tile2adj(tleft,tright=None,sep=0,overlap=None):
    if isinstance(tleft[0],dict):
        tleft = map(tile_flatten,tleft)
    if tright is None:
        tright = tleft        
    elif isinstance(tright[0],dict):
        tright = map(tile_flatten,tright)

    if overlap is None:
        T = tleft[0][0]
        overlap = 2*T - sep
    tleft = np.array(tleft)[:,2:]
    tright = np.array(tright)[:,2:]
    #### construct DAG from tiles
    heads = tright[:,:(overlap)]
    tails = tleft[:,-(overlap):]
#     mids  = tiles[:,T:-T]
    ##### tail of the left is the head of the right
    ##### axis= 0 is left, axis=1 is right
    adj = tails[:,None] == heads[None,:]
    adj = np.all(adj,axis=2)#.squeeze()
    return adj

N = 1000
def iter_head(cks,N):
    i = 0
    lst = []
    for x in cks:
        i+=1
        lst+=[x]
        if i==N:
            break
    return lst
def pre2curr(pre,mid=0):
    if isinstance(pre[0],dict):
        pre = map(tile_flatten,pre)
    out = []    
    for x in pre:
#         T = x[]
        T,per = x[:2]
        move = 0 if (per==0) | mid else  cmp(per,0)*(T//abs(per))
        out.append(x[2+T+move:-T+move])
    return out
#     print pre[:5]
# pre2curr(tile0)
def show_cycle(env,ck,curr,callback = np.transpose,**kwargs):
#     print ck
    ini = np.reshape([curr[x] for x in ck],(1,-1,1))
    out = sample(env,ini=ini,**kwargs)
    print np.shape(out)
    showsptime(callback(out.squeeze()))

# def f2():
# #     X = np.array(tile0)
# #     X = tile0
#     D = spdist.cdist(tile1,tile0,isCompatible)
#     print D.shape
#     return D
# print len(tile0[0])
# %time f2()
# {x['seq'] for x in tile1} - {x['seq'] for x in tile0}
# tile1
