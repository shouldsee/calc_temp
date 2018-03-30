from KBs import *
import scipy.spatial.distance as spdist
def worker0323(dct):
    sysX = guess(dct=dct)
    hist = sample(sysX)
    hist = hist.reshape(hist.shape[:2]+(-1,))

    d = spdist.pdist(hist[-1],'hamming')
    d = 1 - abs(2*d-1)
    D = spdist.squareform(d)
    np.fill_diagonal(D,2)
    
    d = spdist.pdist(hist[len(hist)//2],'hamming')
    d = 1 - abs(2*d-1)
    D1= spdist.squareform(d)
    np.fill_diagonal(D1,2)
    
    MIN = D.min(axis=0)
    MIN1 = D1.min(axis=0)
    data = np.vstack([MIN1,MIN]).T
    
    MEDS = [np.median(MIN1),np.median(MIN)]
    COV = np.cov(data.T)
    COR = cov2cor(COV)
    return {'rule':{'family':sysX.familyname,'rulestr':sysX.rulestr},
            'data':{ 'med':[x.tolist() for x in MEDS],'cov':COV.ravel().tolist(),'cor':[COR[0,1]]},
           }


import matplotlib.pyplot as plt
def test0323(**kwargs):
    sysX = guess(**kwargs)
    hist = sample(sysX)
    hist = hist.reshape(hist.shape[:2]+(-1,))
    d = spdist.pdist(hist[-1],'hamming')
    d = 1 - abs(2*d-1)
    D = spdist.squareform(d)
    np.fill_diagonal(D,2)
    d = spdist.pdist(hist[len(hist)//2],'hamming')
    d = 1 - abs(2*d-1)
    D1= spdist.squareform(d)
    # plt.imshow(D[:50,:50])
#     plt.hist(D.ravel())
#     plt.hist(d.ravel(),bins=np.linspace(0,1,20))
    MIN = D.min(axis=0)
    MED = np.median(D,axis=0)
    MEAN = np.mean(D,axis=0)
    BINS=np.linspace(0,1,30)
    np.fill_diagonal(D,0)

#     plt.hist(MIN,bins=np.linspace(0,1,20))
#     plt.plot(MIN,MED,'x')

#     plt.hist2d(STD,MED,bins=BINS,norm=None
#     plt.hist2d(MIN,MED,bins=BINS,norm=None
#               )
#     plt.hist2d(D1.ravel(),D.ravel(),bins=BINS,norm=None
#               )
    np.fill_diagonal(D1,2)
    MIN1 = D1.min(axis=0)
    MEDS = [np.median(MIN1),np.median(MIN)]
    plt.hist2d(MIN1,MIN,bins=BINS,norm=None,normed=1
              )
    plt.plot([0,1],[0,1],'r--')
    data = np.vstack([MIN1,MIN]).T
#     res = gaussfit(data)
#     plt.plot(*(res.means_.ravel().tolist()+['rx']))
    plt.plot(*(MEDS+['wx']))
#     COV = res.covariances_[0]
    COV = np.cov(data.T)
    COR = cov2cor(COV)
#     logp = res.score_samples(data)
    plt.title('%.2f %.3f %.3f'%(
#         res.bic(data),
        abs(np.diff(MEDS)),
        COR[0,1],
#         np.std(logp)/np.mean(logp),
        np.trace(COV),
#                            np.prod(np.diag(np.sqrt(COV) ))
                          ) )
    plt.xticks([], [])
#                mpl.colors.LogNorm()
#     plt.hist2d(MEAN,MED,bins=BINS)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.grid()
    return D

    return {'rule':{'family':sysX.family,'rulestr':sysX.rulestr},
            'med':np.ravel(MEDS).tolist(),'cov':COV.ravel().tolist(),'cor':COR[0,1]}


# def worker0325(**kwargs):
from pymisca.util import curve_fit_wrapper
def worker0325(dct,ps=np.array([0.1   , 0.01  , 0.001 , 0.0001, 0.    ])
              ,as_raw = 0):
#     ps = np.array([0.1   , 0.01  , 0.001 , 0.0001, 0.    ]) 
    def model_exp(x, x0, bt, c):
        return c*np.exp(x/(-bt)) + x0
    #     return c*np.exp(-bt*x) + x0

    # ys = arr[0]
    def fit_exp(ys,xs = None):
        if xs is None:
            xs=  np.arange(ys.size)
        popt,pcov,yfit = curve_fit_wrapper(model_exp, xs, ys,plot=0)
        loss = np.mean((yfit-ys)**2)
        return popt,yfit,loss
    def main(env,ps=ps,agg=np.min,as_raw=0):
    #     ps = np.array([0.1   , 0.01  , 0.001 , 0.0001, 0.    ])
        lst = []
        for pr in ps:
            adv = mix_adv(fill_ber,env.adv,pa=pr)
            hist = sample(env,adv=adv)
            hist = hist.reshape(hist.shape[:-2]+(-1,))
            dlst=  []
            for x in hist:
                d= spdist.pdist(x,'hamming')
                d = hill(d)
                D = spdist.squareform(d)
                dlst+=[D]        
                np.fill_diagonal(D,2)    
            lst.append(agg(dlst,axis=(-1)))
        lst=  np.array(lst)
        if as_raw:
            return lst
        else:            
            opt = post(lst)
            out = np.vstack([[ps],opt])
        return out
    def post(o,ps=None,ylim=[0,150],axs = None,silent=0,lab=''):
        arr = np.mean(o,axis=-1)
        out = map(lambda x:fit_exp(x)[0],arr) 
        #### out = (popt,yfit,loss)
        return zip(*out)    
    env = guess(dct=dct)
    env.change_size((128,128,32**2))
    out = main(env,as_raw=as_raw)
    return out
#     plt.show()
    
test = test0323