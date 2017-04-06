import csv,pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from mpld3 import plugins
import mpld3
from mpld3 import utils
from mpl_toolkits.mplot3d import Axes3D
from utils import *

# %matplotlib inline
# mpld3.enable_notebook()


class ClickInfo(plugins.PluginBase):
    """Plugin for getting info on click"""
    
    JAVASCRIPT = """
    mpld3.register_plugin("clickinfo", ClickInfo);
    ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
    ClickInfo.prototype.constructor = ClickInfo;
    ClickInfo.prototype.requiredProps = ["id","labels","rules"];
    function ClickInfo(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };
    
    ClickInfo.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);
        var labels = (this.props.labels);
        var rules = (this.props.rules);
        
        obj.elements().on("mousedown",
                          function(d, i){
                          txt=labels[i];
                          window.prompt("You clicked Point "+ i + ", Ctrl+C to copy to clipboard, Click 'OK' or 'Cancel' to open the CA in a new pop-up.   Rulestring:", txt);
                            
                            rule=rules[i];

//                            var s = template.formatUnicorn(rule,soup);
//                            var s = 'bbbbbboooooooo!';
//                            var divs=div_template.formatUnicorn(s);
//                            document.getElementById("viewer").innerHTML = s;
//                            document.getElementById("viewer").visibility = "show";
//                            document.getElementById("viewer")
                            window.open("/view.php?rule_alias="+rule);

//                            var sp1 = document.createElement('textarea');
//                            elementText = document.createTextNode(s);                            
//                            sp1.appendChild(elementText);

//                            var sp2 = document.getElementById("textarea");
//                            var parentDiv = sp2.parentNode;
//                            parentDiv.replaceChild(sp1, sp2);

//                            var cv1=document.createElement('canvas')
//                             cv1.appendChild(document.createTextNode(''));
//                            cv1.setAttribute('width','480');
//                            cv1.setAttribute('height','480');

                            var newviewer=document.createElement('div');
                            newviewer.setAttribute('class','viewer');
                            newviewer.setAttribute('id','viewer');
                            newviewer.appendChild(sp1);
                            newviewer.appendChild(cv1);

//                            newviewer.appendChild(document.getElementById('cv1'))
                            document.body.appendChild(newviewer);
//                            parentDiv.parentNode.appendChild(newviewer);

                            document.getElementById('viewer').contentWindow.location.reload();

//                            viewer.innerHTML=s;
alert(txt);
                          //document.getElementById("viewer").innerHTML = rule;

                          
                          });
    }
    
    
    """
    
#     obj.elements().on("mousedown",
#                           function(d, i){alert("clicked on points[" + labels[i] + "]");});
    def __init__(self, points,labels=None,rules=None):
        self.dict_ = {"type": "clickinfo",
                      "id": utils.get_id(points),
                     "labels":labels,
                     "rules":rules};
    

    
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
    
    
# def repack(oldrule):
#     helper1 = [0]*2;

#     for i in range(2):
#         helper1[i] = [
#             { "0": 0 },
#             { "c": 0, "e": 0    },
#             { "a": 0, "c": 0, "e": 0, "i": 0, "k": 0, "n": 0    },
#             { "a": 0, "c": 0, "e": 0, "i": 0, "j": 0, "k": 0, "n": 0, "q": 0, "r": 0, "y": 0 },
#             { "a": 0, "c": 0, "e": 0, "i": 0, "j": 0, "k": 0, "n": 0, "q": 0, "r": 0, "t": 0, "w": 0, "y": 0, "z": 0 },
#             { "a": 0, "c": 0, "e": 0, "i": 0, "j": 0, "k": 0, "n": 0, "q": 0, "r": 0, "y": 0 },
#             { "a": 0, "c": 0, "e": 0, "i": 0, "k": 0, "n": 0    },
#             { "c": 0, "e": 0    },
#             { "0": 0 }
#         ]

#     state = ''
#     survive = 1
#     direction = 1
#     oldrule += '.'
#     for char in oldrule:
#         if char in '012345678./_Ss':
#             if char != state:
#                 if state and state in '012345678' and 0 == max([i[1] for i in helper1[survive][int(state)].items()]):
#                     for j, k in helper1[survive][int(state)].items():
#                         helper1[survive][int(state)][j] = 1
#                 state = char
#             if char in 'sS':
#                 survive = 1
#             elif char in '/_':
#                 survive = 1 - survive
#             direction = 1
#         elif char.lower() in 'aceijknqrtwyz':
#             helper1[survive][int(state)][char.lower()] = direction
#         elif char == '-':
#             direction = 0
#             for i in helper1[survive][int(state)].items():
#                 helper1[survive][int(state)][i[0]] = 1
#         elif char.lower() =='b':
#             survive = 0
#             direction = 1

#     newrule = "B"
#     for base in range(2):
#         for state in range(9):
#             helper2 = [i[1] for i in helper1[base][state].items()]
#             if 1 == max(helper2):
#                 helper3 = ''
#                 if 0 == min(helper2):
#                     if helper2.count(1)/(1.0*len(helper2))<=0.501:
#                         helper3 = [j for j, k in helper1[base][state].items() if ((k==1) and (j!='0'))]
#                         helper3.sort()
#                         helper3 = ''.join(helper3)
#                     else:
#                         helper3 = [j for j, k in helper1[base][state].items() if ((k==0) and (j!='0'))]
#                         helper3.sort()
#                         helper3 = '-' + ''.join(helper3)
#                 newrule += str(state) + helper3
#         if base == 0:
#             newrule += '/S'
#     return newrule

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
    rules=list(repack(cel.split('_')[-1]) for cel in data[:,0]);
    
    # labels=data[:,[0,1,3]].T.to_html



    # fig, ax = plt.subplots(subplot_kw=dict(axisbg='#DDDDDD'
    #                                        ,projection='3d'
                                          # ))
    fig.set_size_inches([5,4])
    ax.grid(color='white', linestyle='solid')
#    ax.set_ylim(0,0.38)
#    ax.set_xlim(0,1)
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
                    ClickInfo(sct,labels,rules)
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
#    mpld3.display(fig)
    return( fig,ax,fig2,ax2)