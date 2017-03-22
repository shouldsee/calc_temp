#import sys
#import os
#sys.path.append(os.path.abspath('..'))
#from utils import *

import numpy as np
import math as m
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.integrate import odeint
from functools import reduce
import csv
import time
import pickle
import copy
# %matplotlib inline
from scipy.interpolate import *
from IPython.display import HTML

tog='''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''';
HTML(tog)

base2bin=lambda data,scale,num_of_bits: bin(int(data, scale))[2:].zfill(num_of_bits);
hex2bin=lambda hexdata,num_of_bits: base2bin(hexdata,16,num_of_bits);

def csv2dat(fname):
    dat=[];
    with open(fname, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in (spamreader):
            dat+=[row];

    return np.array(dat);

def init_esplot():
    plt.close('all');
    fig=plt.figure(figsize=[10, 4]);
    ax=plt.subplot(1,1,1)
    return(ax,fig)

def vfield(axis,Ndot,num=20,scale=1/0.0015,norm_method='none',col=None):
    xlim=list(axis.get_xlim());
    ylim=list(axis.get_ylim());
    x=np.linspace(xlim[0],xlim[1],num);
    y=np.linspace(ylim[0],ylim[1],num);
    xs,ys=np.meshgrid(x,y);
    us,vs=Ndot(xs,ys);
    
    ls=(us**2+vs**2)**0.5;        
    if norm_method=='log':
        lls=np.min(np.log(ls),0);
        us=us/ls*lls;
        vs=vs/ls*lls;
    elif norm_method=='len':
        ls=(us**2+vs**2)**0.5;
        us=us/ls;
        vs=vs/ls;
    axis.quiver(xs,ys,us,vs,color=col,scale_units='inches',angles='xy',pivot='mid',scale=scale)

class intobj():
    def __init__(self,Ndot,N0,params):
        self.fcn=Ndot;
        self.ss,self.labels=N0;
        self.params=params;
    def evo(self,ts):
        self.ts=ts;
        Ns=odeint(self.fcn,self.ss,ts,args=(self.params,));
        self.Ns=Ns;
        return(Ns)
    def line(self,ax,idx):
        ax.plot(self.ts,self.Ns[:,idx],label=self.labels[idx]);
    def phase(self,ax,idx):
        xi,yi=idx;
        ax.plot(self.Ns[:,xi],self.Ns[:,yi]);
        ax.set_xlabel(self.labels[xi]);
        ax.set_ylabel(self.labels[yi]);
        


def readcsv(fname):
#     fname='measles_data.csv'
    csvdata={};

    with open(fname,'r') as  f:
        header=f.readline().rstrip('\n').split(',');
        lsts=[[]]*(len(header));
        for line in f.readlines():
            data=line.rstrip('\n').split(',');
            for i,k in enumerate(data):
    #             len(lsts)
                lsts[i]=lsts[i]+[float(k)];
    #     print(lsts)
        for i,lst in enumerate(lsts):
            csvdata[header[i]]=lst;
    #     print(len(lsts))
    return csvdata;



def march(yiter,ytnow,dt,params):
    ynow,tnow=ytnow;
    yout=yiter(ynow,tnow,params);
    tout=tnow+dt;
    return (yout,tout);


class state():
    def __init__(self,yiter,yt,dt):
        self.yiter=yiter
        self.dt=dt;
        self.yt=np.array(yt);
#         self.t=0;
        self.ys=[yt[0]];
        self.ts=[yt[1]];
#         self.ts=np.array();
    def get_params(self):
        pass
    def forward(self,dur):
        ts=np.arange(self.yt[1],self.yt[1]+dur,self.dt);
        for t in ts:
            self.yt=march(self.yiter,
                          self.yt,
                          self.dt,
                          self.get_params());
#             print(self.ys)
            self.ys=np.vstack((np.array(self.ys) ,
                                np.array(self.yt[0]) ))
        self.ts =self.ts + list(ts);
                    
### Testing
# k=1./150;
# k=1./10;
# # s0=state(yiter,[(10.,5.),0.],lambda : 10);

# s0=state(yiter,[(10.,5.),0.],lambda : random.expovariate(k));

# ## create an ensemble of size 1000.
# ss=[];
# for i in range(200):
#     ss.append(copy.copy(s0));
# ss_t0=ss[:];
    
# for s in ss:
#     s.forward(200);
# # ss[0].forward(100)
# maxit=max(len(s.ys[:,0]) for s in ss);
# ss[100].ts

# (ax,fig)=init_esplot();

# ax1=plt.subplot(2,2,1);
# ax1.set_xlim(0,200)
# ax1.set_ylim(0,10)
# for s in ss:
#     ax1.plot(s.ts,s.ys[:,0]);
    

    
# ax1.set_title('dt=random.expovariate(1./10)')


# s0=state(yiter,[(10.,5.),0.],lambda : 10);
# ## create an ensemble of size 1000.
# ss=[];
# for i in range(200):
#     ss.append(copy.copy(s0));
# ss_t0=ss[:];
# for s in ss:
#     s.forward(200);
# # ss[0].forward(100)
# maxit=max(len(s.ys[:,0]) for s in ss);
# ss[100].ts
# ax2=plt.subplot(2,2,2);
# pop100=list(s.ys[-1,0]+0.5*np.random.random(s.ys[-1,0].shape) for s in ss)
# for s in ss:
#     ax2.plot(s.ts,s.ys[:,0]);
    
# ax2.set_title('dt=10')