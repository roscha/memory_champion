import neurodesign
from neurodesign import generate

##phase1
EXP = neurodesign.experiment(
TR=1.1,
n_trials=72,
P = [54/72.,18/72.],
C = [[1,-1],[1,0]],
n_stimuli = 2,
rho=0.3,
stim_duration=1,
t_post=.5,
ITImodel = 'uniform',
ITImin = 0,
ITImax=0.5
)

POP = neurodesign.optimisation(
experiment=EXP,
weights=[0,0.5,0.25,0.25],
preruncycles = 1000,
cycles = 1000,
outdes = 10,
folder = "D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/",
optimisation='GA'
)
POP.optimise()



##phase2
EXP2 = neurodesign.experiment(
TR=1.1,
n_trials=72,
P = [18/72.,18/72.,18/72.,6/72.,6/72.,6/72.],
C = [[1,0,0,-1,0,0],[0,1,0,0,-1,0],[0,0,1,0,0,-1]],
n_stimuli = 6,
rho=0.3,
stim_duration=2,
t_post=.5,
ITImodel = 'uniform',
ITImin = 0,
ITImax=0.5
)

POP2 = neurodesign.optimisation(
experiment=EXP2,
weights=[0,0.5,0.25,0.25],
preruncycles = 1000,
cycles = 1000,
outdes = 10,
folder = "D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/",
optimisation='GA'
)
POP2.optimise()




with open('D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/memchampriondeck/designs/design.txt','w') as f:
    f.write('var ITIs1 = [['+'],['.join([','.join([np.str(j) for j in i.ITI]) for i in POP.designs])+']];\n')
    f.write('var orders1 = [['+'],['.join([','.join([np.str(j) for j in i.order]) for i in POP.designs])+']];\n')
    f.write('var ITIs2 = [['+'],['.join([','.join([np.str(j) for j in i.ITI]) for i in POP2.designs])+']];\n')
    f.write('var orders2 = [['+'],['.join([','.join([np.str(j) for j in i.order]) for i in POP2.designs])+']];')


##### this is absolutely not adapted to this type of task
import numpy as np
import random

import copy

#for the list of cards 
for d in range(10):
    listcard=np.arange(52)
    random.shuffle(listcard)
    setini = [listcard[:18],listcard[18:18+17],listcard[18+17:]]
    
    for i in range(3):
        if i==0:
            setlist1=copy.deepcopy(setini)
            setall=[]
            #print(setlist)
            for i in range(4):
                random.shuffle(setlist1[0])
                random.shuffle(setlist1[1])
                random.shuffle(setlist1[2])
                setlist=copy.deepcopy(setlist1)
                setlist[1]=np.concatenate([setlist[1],[52]],0)
                setlist[2]=np.concatenate([setlist[2],[53]],0)
                #print(setlist)
                setall+=[copy.deepcopy(setlist)]
            print(setall)
        if i==1:
            setini1=copy.deepcopy(setini)
            setlist1=[np.concatenate([setini1[1][:9],setini1[2][:9]],0),np.concatenate([setini1[0][:9],setini1[2][9:]],0),np.concatenate([setini1[0][9:],setini1[1][9:]],0)]
            setall=[]
            #print(setlist)
            for i in range(4):
                random.shuffle(setlist1[0])
                random.shuffle(setlist1[1])
                random.shuffle(setlist1[2])
                setlist=copy.deepcopy(setlist1)
                setlist[1]=np.concatenate([setlist[1],[52]],0)
                setlist[2]=np.concatenate([setlist[2],[53]],0)
                #print(setlist)
                setall+=[copy.deepcopy(setlist)]
            print(setall)
        if i==2:
            setini1=copy.deepcopy(setini)
            setlist1=[np.concatenate([setini1[1][9:],setini1[2][8:]],0),np.concatenate([setini1[0][9:],setini1[2][:8]],0),np.concatenate([setini1[0][:9],setini1[1][:9]],0)]
            setall=[]
            #print(setlist)
            for i in range(4):
                random.shuffle(setlist1[0])
                random.shuffle(setlist1[1])
                random.shuffle(setlist1[2])
                setlist=copy.deepcopy(setlist1)
                setlist[0]=np.concatenate([setlist[0],[52]],0)
                setlist[1]=np.concatenate([setlist[1],[53]],0)
                #print(setlist)
                setall+=[copy.deepcopy(setlist)]
            print(setall)


####for multieccho data 
import neurodesign
from neurodesign import generate
import numpy as np
##phase1
EXP = neurodesign.experiment(
TR=1.76,
n_trials=72,
P = [54/72.,18/72.],
C = [[1,-1],[1,0]],
n_stimuli = 2,
rho=0.3,
stim_duration=1,
t_post=.5,
ITImodel = 'uniform',
ITImin = 0,
ITImax=0.5
)

POP = neurodesign.optimisation(
experiment=EXP,
weights=[0,0.5,0.25,0.25],
preruncycles = 1000,
cycles = 1000,
outdes = 10,
folder = "D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/",
optimisation='GA'
)
POP.optimise()



##phase2
EXP2 = neurodesign.experiment(
TR=1.76,
n_trials=72,
P = [18/72.,18/72.,18/72.,6/72.,6/72.,6/72.],
C = [[1,0,0,-1,0,0],[0,1,0,0,-1,0],[0,0,1,0,0,-1]],
n_stimuli = 6,
rho=0.3,
stim_duration=2,
t_post=.5,
ITImodel = 'uniform',
ITImin = 0,
ITImax=0.5
)

POP2 = neurodesign.optimisation(
experiment=EXP2,
weights=[0,0.5,0.25,0.25],
preruncycles = 1000,
cycles = 1000,
outdes = 10,
folder = "D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/",
optimisation='GA'
)
POP2.optimise()




with open('D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/memchampriondeck/designs/design_ME.txt','w') as f:
    f.write('var ITIs1 = [['+'],['.join([','.join([np.str(j) for j in i.ITI]) for i in POP.designs])+']];\n')
    f.write('var orders1 = [['+'],['.join([','.join([np.str(j) for j in i.order]) for i in POP.designs])+']];\n')
    f.write('var ITIs2 = [['+'],['.join([','.join([np.str(j) for j in i.ITI]) for i in POP2.designs])+']];\n')
    f.write('var orders2 = [['+'],['.join([','.join([np.str(j) for j in i.order]) for i in POP2.designs])+']];')

