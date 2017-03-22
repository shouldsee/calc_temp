import numpy as np
import pickle
from astropy.convolution import convolve

base2bin=lambda data,scale,num_of_bits: bin(int(data, scale))[2:].zfill(num_of_bits);
hex2bin=lambda hexdata,num_of_bits: base2bin(hexdata,16,num_of_bits);
convolve_int=lambda a,fir,method:np.around(convolve(a,fir,method)).astype(np.int);

henseldict=['b0_','b1c','b1e','b2a','b2c','b3i','b2e','b3a','b2k','b3n','b3j','b4a','s0_','s1c','s1e','s2a','s2c','s3i','s2e','s3a','s2k','s3n','s3j','s4a','b2i','b3r','b3e','b4r','b4i','b5i','s2i','s3r','s3e','s4r','s4i','s5i','b2n','b3c','b3q','b4n','b4w','b5a','s2n','s3c','s3q','s4n','s4w','s5a','b3y','b3k','b4k','b4y','b4q','b5j','b4t','b4j','b5n','b4z','b5r','b5q','b6a','s3y','s3k','s4k','s4y','s4q','s5j','s4t','s4j','s5n','s4z','s5r','s5q','s6a','b4e','b5c','b5y','b6c','s4e','s5c','s5y','s6c','b5k','b6k','b6n','b7c','s5k','s6k','s6n','s7c','b4c','b5e','b6e','s4c','s5e','s6e','b6i','b7e','s6i','s7e','b8_','s8_',];
rca2ntca=[0, 1, 2, 3, 1, 4, 3, 5, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 13, 16, 15, 17, 14, 15, 18, 19, 20, 21, 22, 23, 2, 8, 6, 10, 3, 9, 7, 11, 24, 25, 26, 27, 25, 28, 27, 29, 14, 20, 18, 22, 15, 21, 19, 23, 30, 31, 32, 33, 31, 34, 33, 35, 1, 4, 8, 9, 36, 37, 38, 39, 3, 5, 10, 11, 38, 39, 40, 41, 13, 16, 20, 21, 42, 43, 44, 45, 15, 17, 22, 23, 44, 45, 46, 47, 8, 48, 49, 50, 38, 51, 52, 53, 25, 54, 55, 56, 57, 58, 59, 60, 20, 61, 62, 63, 44, 64, 65, 66, 31, 67, 68, 69, 70, 71, 72, 73, 2, 8, 24, 25, 8, 48, 25, 54, 6, 10, 26, 27, 49, 50, 55, 56, 14, 20, 30, 31, 20, 61, 31, 67, 18, 22, 32, 33, 62, 63, 68, 69, 6, 49, 26, 55, 10, 50, 27, 56, 26, 55, 74, 75, 55, 76, 75, 77, 18, 62, 32, 68, 22, 63, 33, 69, 32, 68, 78, 79, 68, 80, 79, 81, 3, 9, 25, 28, 38, 51, 57, 58, 7, 11, 27, 29, 52, 53, 59, 60, 15, 21, 31, 34, 44, 64, 70, 71, 19, 23, 33, 35, 65, 66, 72, 73, 10, 50, 55, 76, 40, 82, 59, 83, 27, 56, 75, 77, 59, 83, 84, 85, 22, 63, 68, 80, 46, 86, 72, 87, 33, 69, 79, 81, 72, 87, 88, 89, 1, 36, 8, 38, 4, 37, 9, 39, 8, 38, 49, 52, 48, 51, 50, 53, 13, 42, 20, 44, 16, 43, 21, 45, 20, 44, 62, 65, 61, 64, 63, 66, 3, 38, 10, 40, 5, 39, 11, 41, 25, 57, 55, 59, 54, 58, 56, 60, 15, 44, 22, 46, 17, 45, 23, 47, 31, 70, 68, 72, 67, 71, 69, 73, 4, 37, 48, 51, 37, 90, 51, 91, 9, 39, 50, 53, 51, 91, 82, 92, 16, 43, 61, 64, 43, 93, 64, 94, 21, 45, 63, 66, 64, 94, 86, 95, 9, 51, 50, 82, 39, 91, 53, 92, 28, 58, 76, 83, 58, 96, 83, 97, 21, 64, 63, 86, 45, 94, 66, 95, 34, 71, 80, 87, 71, 98, 87, 99, 3, 38, 25, 57, 9, 51, 28, 58, 10, 40, 55, 59, 50, 82, 76, 83, 15, 44, 31, 70, 21, 64, 34, 71, 22, 46, 68, 72, 63, 86, 80, 87, 7, 52, 27, 59, 11, 53, 29, 60, 27, 59, 75, 84, 56, 83, 77, 85, 19, 65, 33, 72, 23, 66, 35, 73, 33, 72, 79, 88, 69, 87, 81, 89, 5, 39, 54, 58, 39, 91, 58, 96, 11, 41, 56, 60, 53, 92, 83, 97, 17, 45, 67, 71, 45, 94, 71, 98, 23, 47, 69, 73, 66, 95, 87, 99, 11, 53, 56, 83, 41, 92, 60, 97, 29, 60, 77, 85, 60, 97, 85, 100, 23, 66, 69, 87, 47, 95, 73, 99, 35, 73, 81, 89, 73, 99, 89, 101];
rca2ntca=np.array(rca2ntca,np.int);
henselidx={k: v for v, k in enumerate(henseldict)};
subconf='_cekainyqjrtwz';
with open('tp','rb') as f:  # Python 3: open(..., 'rb')
    hdist, tst_data = pickle.load(f)
    hdist = np.array(hdist).reshape([512,512]);

def add_all(s,prime,sold,neg=0):
    for c in subconf:
        conf=prime+sold+c;
        try:
            s[henselidx[conf]]=str(1-neg);
        except KeyError:
            pass
class kb_2dntca():
    def __init__(self):
        pass
    def rulestr2alias(self, rulestr):
        r=hex2bin(rulestr,102);
        r=r[::-1];
        rule=[i for x,i in zip(r,range(len(r))) if x=='1'];
        rs=[];
        alias='';
        others=[];
        # ps=1;
        primed=0;
        for i in rule:
            s=henseldict[i];
            alias=alias.rstrip('_');

            if primed:
                if s[0]==sold[0]:
                    if s[1]==sold[1]:
                        alias+=s[2]
                    else:
                        alias+=s[1:];
                        primed=1;
                else:
                    others.append(s);
                    # pass
                    # break
                    continue
            else:
                alias+=s;
                primed=1;
            sold=s;
        alias=alias.rstrip('_');
        primed=0;
        for s in others:
            alias=alias.rstrip('_');
            if primed:
                if s[0]==sold[0]:
                    if s[1]==sold[1]:
                        alias+=s[2]
                    else:
                        alias+=s[1:];
                        primed=1;
                else:
                    others.append(s);
                    # pass
                    # break
                    continue
            else:
                alias+=s;
                primed=1;
            sold=s;
        alias=alias.rstrip('_');
        return alias
    def alias2rulestr(self, ali):
        ali=ali.replace('/','').lower();
        self.s=['0']*102;
        while True:
            prime=ali[0];
            ali=ali[1:];
            sold=[];
            # sold=ali[0];
            # nold=
            neg=0;
            for i,s in enumerate(ali):
                if s.isdigit(): 
                    neg=0;      
                    if sold==[]:
                        pass
                    elif sold.isdigit():
                        add_all(self.s,prime,sold);
                        # golly.note('added all of '+prime+sold)
                    nold=s;

                elif s in ['b','s']:
                    ali=ali[i:];
                    break
                elif s=='-':
                    neg=1;
                    add_all(self.s,prime,nold);
                    # golly.note('added all of '+prime+sold)
                else:
                    conf=prime+nold+s;
                    self.s[henselidx[conf]]=str(1-neg);
                    # golly.note('added '+conf)
                alii=ali[i+1:];
                sold=s;
                # golly.note(alii)  
            if sold.isdigit():
                add_all(self.s,prime,sold);
                # golly.note('added all of '+prime+s)
            if i+1==len(ali):
                break
        ruleprj=''.join(self.s[::-1]);
        rulestr=hex(int(ruleprj,2)).lstrip('0x').rstrip('L').zfill(26);
        return rulestr
    def rulestr2adv(self,rulestr):
        ruleprj=np.array( 
            list(hex2bin(rulestr,102)[::-1]),
            np.int);
#         ruleprj=np.array(list(hex2bin(rulestr,102)[::-1]));
        fir=(2**np.arange(0,9)).reshape([1,3,3]);
        pj=rca2ntca;
        def adv(a,horizon):
            return ruleprj[pj[convolve_int(a,fir,'wrap').astype(np.int)]]
        # adv=lambda a, horizon: ruleprj[pj[convolve_int(a,fir,'wrap').astype(np.int)]]
        return adv  
  
    
    
    
    
class kb_2dtca():
#     def rulestr2alias(rulestr):
#         r=base2bin(int(rulestr),18,2);
#         r=r[:1:-1];
#         r+='0'*(18-len(r));
#         rule=[i for x,i in zip(r,range(len(r))) if x=='1'];
#         alias='b';
#         ps=1;
#         for a in rule:
#             if a>8 and ps:
#                 alias+='s';
#                 ps=0;
#             alias+=str((a)%9)
#         if ps==1:
#             alias+='s';
#         return alias        
    def alias2rulestr(self, ali):
        rule=['0']*18;
        ali=ali.replace('/','').lower().lstrip('b');
        (b,s)=ali.split('s');
        lst=list(str(int(i)+9) for i in s);
        bs=list(b)+(lst)
        for i in bs:
            rule[int(i)]='1';
        rnum=(''.join(rule[::-1]),2);
        return(rnum);
    def rulestr2adv(self,rulestr):
        #take an numpy array and convolution across the axis=[1,2];
        # project the convolved array back to value space according to the rule
        # 
        hex2bin(rulestr)
                                       
class CA_sys():
    def __init__(self,familyname,rulestr,dimsiz,adv=None,rdf=None):
#         siz=[600,100,400];
        self.familyname=familyname;
        self.rulestr=rulestr;
        self.adv=adv;
        self.dimsiz=dimsiz;
        self.change_size();
        if rdf==None:
            self.rdf=lambda:np.random.random(self.siz)<=0.5;

    def change_size(self,dimsiz=None):
        if dimsiz==None:
            dimsiz=self.dimsiz;
        N,hmax,ksq=dimsiz
        self.N=N;
        self.hmax=hmax;
        dd=int(ksq**0.5);
        self.siz = (N,dd,dd);
        
    def rulestr2alias(self):
        kb=eval('kb_'+self.familyname);
        self.alias=kb.rulestr2alias(kb,self.rulestr);
        self.adv=kb.rulestr2adv(kb,self.rulestr);
    def alias2rulestr(self):
        kb=eval('kb_'+self.familyname);
        self.rulestr=kb.alias2rulestr(self.alias)
        self.adv    =kb.rulestr2adv(self.rulestr)            
#     def change_adv(familyname,rulestr):

kb=kb_2dntca();
# kb.rulestr2alias('000000000060031c61c67f86a0')
kb.alias2rulestr('b3/s23')

    
# @function
def measure_temperature(sys0=None,hdist=None,*args,**kwargs):
#     varargin = measure_temperature.varargin
#     nargin = measure_temperature.nargin
    
    sysX=copy.copy(sys0)
    jmax=sysX.N;
    avi=sysX.rdf()
    siz=avi.shape
    siz=(sysX.hmax,)+siz;
    tmp=np.zeros(siz)
    smtmp=np.zeros(siz)

    avc=avi
    i=0
    fir=np.reshape(2 ** (np.arange(0,9)),[1,3,3])
    trans=6
    mtp=0
    stp=0
    while i+1 < sysX.hmax:

        i=i + 1
        avcnew=(sysX.adv(avc,i))
        cavc=convolve_int(avc,fir,'wrap').astype(np.int);
        cavcnew=convolve_int(avcnew,fir,'wrap').astype(np.int);
        idx=np.ravel_multi_index((cavc,cavcnew),[2**9,2**9]);
        tmp[i,:,:,:]=np.expand_dims(hdist.flat[idx],0)
        if i >= trans:
            smtmpnow=np.mean(tmp[i - trans:i,:,:,:],axis=0)
            smtmp[i - trans,:,:,:]=smtmpnow
            if i >= trans + 10:
                mtp=np.mean(smtmpnow.flat)
                stpmat=((smtmp[i - trans,:,:,:] - smtmp[i - trans - trans,:,:,:]))
                a=np.mean(np.abs(stpmat.flat))
                b=abs(np.mean(stpmat.flat))
                stp=a - b
                stp1=np.mean(avcnew.flat)
                stp1=min(stp1,1 - stp1)
        avc=avcnew;
        #     im1=[avc(1,:,:)];
        if mtp < 0.02 and i > 20:
            break
    
    fam_alias=sys0.familyname+'_'+sys0.alias;
# /home/shouldsee/Documents/repos/CA_tfmat/custom_function/measure_temperature.m:55
    # s=sprintf('%s\\t%s\\t%d\\t%f\\t%f\\t%f\\n',fam_alias,num2str(sys0.od),i,mtp,stp,stp1)
    s='{}\t{}\t{:d}\t{:f}\t{:f}\t{:f}\n'.format(fam_alias,sysX.rulestr,i,mtp,stp,stp1)
# /home/shouldsee/Documents/repos/CA_tfmat/custom_function/measure_temperature.m:56
    return s
    
# if __name__ == '__main__':
#     pass
    