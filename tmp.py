 
from KBs import *

def sample(self,t=None,ini=None,adv = None,T = None):    
    if t is None:
        t = {'r2dntca':2,}.get(self.family.familyname,1)
    if T is None:
        T = self.hmax
    if adv is None:
        adv = self.adv
    if ini is None:
        if t>=2:
            ini = np.array([self.rdf().astype(int)]*t)
        else:
            ini=self.rdf().astype(int)
    avc = ini
    hist = np.zeros((T+1+t-1,)+avc.shape[-3:],dtype=np.int)
    
    ###### !!!Be very careful with the indexing in this loop!!!
    for i in range(0,T+1):
        hist[i] = avc[0] if t>=2 else avc
        avc=(adv(avc)) 
    return hist
class kb_r2dntca(kb_2dntca):
    familyname='r2dntca'
#     def __init__(self):
#         self.familyname = 'r2dntca'
#         self=super(kb_r2dntca,self).__init__()
#         return self
#        
    def bin2adv(self, ruleprj):
        if isinstance(ruleprj,str):
            ruleprj = list(ruleprj)
        ruleprj = np.array(ruleprj,np.int)
        def adv(a,horizon=0):
            old = a[0]
            curr = a[1]
            new  = ruleprj[self.conv(curr)]^old
            return np.array([curr,new])
                              
        return adv

        
