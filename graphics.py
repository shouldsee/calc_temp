import csv,pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from mpld3 import plugins
import mpld3
from mpld3 import utils
from mpl_toolkits.mplot3d import Axes3D
#%matplotlib inline
# mpld3.enable_notebook()
class ClickInfo(plugins.PluginBase):
    """Plugin for getting info on click"""
    
    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id","labels"];
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    
    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        var labels = (this.props.labels);
        obj.elements().on("mousedown",
                          function(d, i){
                          txt=labels[i];
                          window.prompt("You clicked Point "+ i + ", Ctrl+C to copy to clipboard, Rulestring:", txt);
                          
                          
                          });
    }
    """
    
#     obj.elements().on("mousedown",
#                           function(d, i){alert("clicked on points[" + labels[i] + "]");});
    def __init__(self, points,labels=None):
        self.dict_ = {"type": "clickinfo",
                      "id": utils.get_id(points),
                     "labels":labels};
    
def put_patches(ax):
    xf1=np.array([0.12,0.4]);
    yf1=np.array([.10,.19]);
    sigma1=np.array([.025]);
    ax.fill_between(xf1,yf1+sigma1, yf1-sigma1, facecolor='green', alpha=0.5,label='Uncond_Comp')


    xf1=np.linspace(.015,.12,50);
    # yf1=np.array([.12,.21]);
    yf1=xf1**0.63/5.7;
    sigma1=.0025+(xf1-0.015)*0.12;
    ax.fill_between(xf1,yf1+sigma1, yf1-sigma1, facecolor='yellow', alpha=0.5,label='Cond_Comp')

    pt1=[.65,.13];
    pt2=[.8,.07];
    pts=np.vstack((pt1,pt2));
    xf1=pts[:,0];
    xf1=np.linspace(xf1[0],xf1[1],50)
    yf1=pts[:,1];
    yf1=np.linspace(yf1[0],yf1[1],50)
    sigma1=.0025+(.8-xf1)*0.26;
    ax.fill_between(xf1,yf1+sigma1, yf1-sigma1, facecolor='red', alpha=0.2,label='Chaos')
def make_figure(figANDax,sample_data):
    fig,ax,fig2,ax2=figANDax
    with open('tp','rb') as f:  # Python 3: open(..., 'rb')
        hdist, tst_data = pickle.load(f)
        hdist = np.array(hdist).reshape([512,512]);

    col=[];
    # data=np.array([[]]);np.array()
    tst_data=np.array(tst_data)
    tst_data=tst_data;
    cm=plt.cm.rainbow
    col=col+list(cm(.01) for i in range(tst_data.shape[0]));

    sample_data=np.array(sample_data)
    col+=list(cm(.9) for i in range(sample_data.shape[0]));
    data=np.vstack((tst_data,sample_data));



    xs=data[:,3];
    xs=xs.astype(np.float)
    xs[np.isnan(xs)]=0;
    ys=(data[:,4].astype(np.float));
    # ys[ys==0]=1;
    # ys=np.log(ys);
    ys[~np.isfinite(ys)]=0;
    zs=(data[:,5].astype(np.float));
    zs[~np.isfinite(zs)]=0;


    sizs=list((.6-float(x))/.00755 for x in data[:,5])
    N = xs.size;
    labels=list(data[:,1]);
    # labels=data[:,[0,1,3]].T.to_html



    # fig, ax = plt.subplots(subplot_kw=dict(axisbg='#DDDDDD'
    #                                        ,projection='3d'
                                          # ))
    fig.set_size_inches([5,4])
    ax.grid(color='white', linestyle='solid')
    ax.set_ylim(0,0.38)
    ax.set_xlim(0,1)
    put_patches(ax)
    sct = ax.scatter(xs,
                     ys,
                     c=col,                
                     s = sizs,
                     alpha=1.0,
    #                      label=labels,
                         cmap=plt.cm.rainbow)
    red_patch = mpatches.Patch(color=plt.cm.rainbow(.98), label='The red data')
    pur_patch = mpatches.Patch(color=plt.cm.rainbow(.02), label='The red data')
    yel_patch = mpatches.Patch(color=plt.cm.rainbow(.02), label='The red data')
    handles, leglabels = ax.get_legend_handles_labels()
    handles +=[red_patch,pur_patch];
    leglabels +=['sample','reference'];
    ax.legend(handles,leglabels)
    ax.set_title("Dynamic landscape, 2D projection", size=20)
    plugins.connect(fig, 
                    plugins.PointLabelTooltip(sct, labels),
    #                 plugins.Zoom(enabled=False),
                    ClickInfo(sct,labels)
                   )
    ax.set_xlabel('Avg Temp',size=15);
    ax.set_ylabel('mean(abs(d_Temp)) - abs(mean(d_Temp))',size=15);
    
    sct3d = ax2.scatter(xs,
                         ys,
                     zs,
                        c=col,
    #                      c=list( 1.*float(i)/N for i in xs),
                         s = sizs,
                         alpha=1.0,
    #                      label=labels,
                         cmap=plt.cm.rainbow)
    ax2.set_title("Dynamic landscape, 3D", size=20)
    ax2.set_xlabel('Avg Temp',size=15);
    ax2.set_ylabel('mean(abs(d_Temp)) - abs(mean(d_Temp))',size=15);
    ax2.set_zlabel('Density of dominating state',size=15);
    mpld3.display(fig)