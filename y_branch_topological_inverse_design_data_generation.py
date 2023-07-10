import numpy as np
import matplotlib.pyplot as plt
import imp
import os
#importlibutil
import random
import time

micron=1e-6
dbu=0.13*micron

X=2.6*micron
Y=2.6*micron

taperX=10*micron
taperYin=0.5*micron
taperYout=1.3*micron
OutTaperSeparation=1.3*micron  #center to center
taperRectLength=1*micron

XN=int(X/dbu)
YN=int(Y/dbu)

lumapi=imp.load_source("lumapi", "C:\\Program Files\\Lumerical\\v212\\api\\python\\lumapi.py")
fdtd=lumapi.FDTD() #hide = True


def generate_pattern():
    pattern=np.random.randint(0, 2, size=(YN, XN))
    #p2=np.random.randint(0, 2, size=(YN, XN))
    #pattern=pattern # + p2
    #pattern[pattern > 0] = 1
    
    all1=np.random.randint(0, YN)
    pattern[all1, :]=1
    all1=np.random.randint(0, YN)
    pattern[all1, :]=1
    
    r=int(0.25*YN)
    for i in  range(r):
        pattern[int(2*r-i):int(2*r+i), r-i-1]=1
        pattern[int(2*r-i)-r:int(2*r+i)-r, i-r]=1
        pattern[int(2*r-i)+r:int(2*r+i)+r, i-r]=1
    
    A=YN*XN
    print('Now=', np.count_nonzero(pattern)/A)
        
    plt.imshow(pattern, cmap='binary') #'gray'
    plt.axis('off')
    return pattern

def add_rect(x, y):
    fdtd.addrect()
    fdtd.set("name","rect")
    fdtd.set('x', x)
    fdtd.set("x span", dbu)
    fdtd.set('y', y)
    fdtd.set('y span', dbu)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 0.22*micron)
    fdtd.set("material","Si (Silicon) - Palik")
    return 

def add_tapers():
    #input_taper
    vtx = np.array([[0,-taperYout/2+dbu/2], [0,taperYout/2+dbu/2], [-taperX, taperYin/2+dbu/2], [-taperX,-taperYin/2+dbu/2]])
    fdtd.addpoly()
    fdtd.set("name","input_taper")
    fdtd.set("vertices",vtx)
    fdtd.set('x', -dbu/2)
    fdtd.set('y', -Y/2)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 0.22*micron)
    fdtd.set("material","Si (Silicon) - Palik")
    
    #input_rect
    fdtd.addrect()
    fdtd.set("name","input_rect")
    fdtd.set('x', -taperX-taperRectLength/2-dbu/2)
    fdtd.set("x span", 1*micron)
    fdtd.set('y', -Y/2+dbu/2)
    fdtd.set('y span', taperYin)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 0.22*micron)
    fdtd.set("material","Si (Silicon) - Palik")
    
    #output_top_taper
    vtx2 = np.array([[0,-taperYin/2+dbu/2], [0,taperYin/2+dbu/2], [-taperX,taperYout/2+dbu/2], [-taperX,-taperYout/2+dbu/2]])
    fdtd.addpoly()
    fdtd.set("name","te_taper")
    fdtd.set("vertices",vtx2)
    fdtd.set('x', X + taperX-dbu)
    fdtd.set('y', -Y/2+OutTaperSeparation/2)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 0.22*micron)
    fdtd.set("material","Si (Silicon) - Palik")
    
    #output_top_rect
    fdtd.addrect()
    fdtd.set("name","output_rect_te")
    fdtd.set('x', X + taperX-dbu+taperRectLength/2)
    fdtd.set("x span", 1*micron)
    fdtd.set('y', -Y/2+OutTaperSeparation/2+dbu/2)
    fdtd.set('y span', taperYin)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 0.22*micron)
    fdtd.set("material","Si (Silicon) - Palik")
    
    #output_bottom_taper
    vtx2 = np.array([[0,-taperYin/2+dbu/2], [0,taperYin/2+dbu/2], [-taperX,taperYout/2+dbu/2], [-taperX,-taperYout/2+dbu/2]])
    fdtd.addpoly()
    fdtd.set("name","tm_taper")
    fdtd.set("vertices",vtx2)
    fdtd.set('x', X + taperX-dbu)
    fdtd.set('y', -Y/2-OutTaperSeparation/2)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 0.22*micron)
    fdtd.set("material","Si (Silicon) - Palik")
    
    fdtd.addrect()
    fdtd.set("name","output_rect_tm")
    fdtd.set('x', X + taperX-dbu+taperRectLength/2)
    fdtd.set("x span", 1*micron)
    fdtd.set('y', -Y/2-OutTaperSeparation/2+dbu/2)
    fdtd.set('y span', taperYin)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 0.22*micron)
    fdtd.set("material","Si (Silicon) - Palik")
    return
    

def add_fdtd():
    fdtd.addfdtd()
    fdtd.set('background material', 'SiO2 (Glass) - Palik')
    fdtd.set('x', X/2)
    fdtd.set("x span", X + 2*taperX +2*taperRectLength-0.5*micron)
    fdtd.set('y', -Y/2)
    fdtd.set("y span", Y + 2*micron)
    fdtd.set('z', 0.0)
    fdtd.set("z span", 2*micron)
    
    #input_port
    fdtd.addport()
    fdtd.set("name","input_port")
    fdtd.set('x', -taperX-taperRectLength/2)
    fdtd.set('y', -Y/2+dbu/2)
    fdtd.set('y span', 2*micron)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 2.5*micron)
    fdtd.select("FDTD::ports::input_port")
    fdtd.set('mode selection', 'fundamental TE mode')
    
    #output_port_top
    fdtd.addport()
    fdtd.set("name","output_te_port")
    fdtd.set('x', X + taperX-dbu+taperRectLength/2)
    fdtd.set('y', -Y/2+OutTaperSeparation/2+dbu/2)
    fdtd.set('y span', 2*micron)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 2.5*micron)
    fdtd.select("FDTD::ports::output_te_port")
    fdtd.set('mode selection', 'fundamental TE mode')  #TE mode
    fdtd.set('direction', 'Backward')
    
    #output_port_bottom
    fdtd.addport()
    fdtd.set("name","output_tm_port")
    fdtd.set('x', X + taperX-dbu/2+taperRectLength/2)
    fdtd.set('y', -Y/2-OutTaperSeparation/2+dbu/2)
    fdtd.set('y span', 2*micron)
    fdtd.set('z', 0.0)
    fdtd.set('z span', 2.5*micron)
    fdtd.select("FDTD::ports::output_tm_port")
    fdtd.set('mode selection', 'fundamental TE mode') #TM mode
    fdtd.set('direction', 'Backward')
    
    #add_frequency_domain_field_and_power_monitor
    fdtd.addpower()
    fdtd.set("name","field_profile")
    fdtd.set("monitor type",7);  # 2D z-normal
    fdtd.set('x', X/2)
    fdtd.set("x span", X + 2*taperX +2*taperRectLength-0.5*micron)
    fdtd.set('y', -Y/2)
    fdtd.set("y span", Y + 2*micron)
    fdtd.set('z', 0.0)
    
    #edit_fdtd_solver
    fdtd.select('FDTD::ports')
    fdtd.set('monitor frequency points', 100);
    fdtd.setglobalsource('wavelength start', 1.5*micron)
    fdtd.setglobalsource('wavelength stop', 1.6*micron)
    
    fdtd.select('FDTD')
    fdtd.set('mesh accuracy', 1)
    fdtd.set('simulation time', 2000e-15)
    
    return

def draw_run_extract():
    fdtd.switchtolayout()
    p=generate_pattern() #structure
    p1=np.argwhere(p>0)
    p1=p1*dbu
    p2=np.diff(p1, axis=0)
    
    N, M=np.shape(p1) #column, row
    add_rect(p1[0][1], p1[0][0])
    for j in range (0, N-1):
        fdtd.copy(p2[j][1], -p2[j][0])
    
    add_tapers()        
    add_fdtd()  
    fdtd.save('structure.fsp')
    #print('Drawing Done')
    
    fdtd.run(3) #1:single processor mode. 2: single processor mode, Pop-up dialogs no longer take focus. 3: parallel mode as defined in the resource manager
    
    #result extraction
    te_port=fdtd.getresult("FDTD::ports::output_te_port", "T")
    tm_port=fdtd.getresult("FDTD::ports::output_tm_port", "T")
    lam=te_port['lambda']
    T_te=te_port['T']
    T_tm=tm_port['T']
    q=np.column_stack((lam, T_te, T_tm)) #characteristics
    
    return p, q


N=2  #number of data point
for i in range (0, N):
    start_time = time.time()
    structure, characteristics=draw_run_extract()
    np.savetxt(r'input_patterns/structure' +str(i)+ '.txt', structure, fmt='%d', delimiter='\t')
    np.savetxt(r'output_characteristics/characteristics' +str(i)+ '.txt', characteristics, delimiter='\t')
    print(i, 'th data. Time:', '{:.2f}'.format((time.time() - start_time)/60), 'minutes')
   
    
    if (i !=N-1):
        fdtd.switchtolayout()
        fdtd.deleteall()
        fdtd.save()
        #fdtd.close()
    
    
    
    