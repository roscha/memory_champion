import neurodesign
from neurodesign import generate
import numpy as np

EXP = neurodesign.experiment(
TR=1.1,
n_trials=44,
P = [1/22.,2/22,3/22,4/22,4/22,4/22,4/22],
C = [[1,1,1,1,1,1,1],[1,1,1,1,1,1,0],[1,1,1,1,1,0,0],[1,1,1,1,0,0,0],[1,1,1,0,0,0,0],[1,1,0,0,0,0,0],[1,0,0,0,0,0,0]],
n_stimuli = 7,
rho=0.3,
stim_duration=7,
t_post=1.5,
ITImodel = 'uniform',
ITImin = 0,
ITImax=1
)

POP = neurodesign.optimisation(
experiment=EXP,
weights=[0,0.5,0.25,0.25],
preruncycles = 100,
cycles = 100,
outdes = 10,
folder = "D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/",
optimisation='GA'
)
POP.optimise()


## random repeat of my stimuli list independantly for each stimuli (N repeatition depending of each initial list length to make 40 items)
## 3 different counter and go get next one in list when it's the stimuli turn in "order"




##need to see about rho, weights and preruncycles and cycles (and define how many design I need)



order=[]
ITI=[]
for i in range(len(POP.designs)):
    order+=[POP.designs[i].order]
    ITI+=[POP.designs[i].ITI]
with open('D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/design.txt','w') as f:
    f.write('var ITIs = [['+'],['.join([','.join([np.str(j) for j in i.ITI]) for i in POP.designs])+']];\n')
    f.write('var orders = [['+'],['.join([','.join([np.str(j) for j in i.order]) for i in POP.designs])+']];')
    

##### this is absolutely not adapted to this type of task



# for multiecho
import neurodesign
from neurodesign import generate
import numpy as np

EXP = neurodesign.experiment(
TR=1.1,
n_trials=44,
P = [1/22.,2/22,3/22,4/22,4/22,4/22,4/22],
C = [[1,1,1,1,1,1,1],[1,1,1,1,1,1,0],[1,1,1,1,1,0,0],[1,1,1,1,0,0,0],[1,1,1,0,0,0,0],[1,1,0,0,0,0,0],[1,0,0,0,0,0,0]],
n_stimuli = 7,
rho=0.3,
stim_duration=7,
t_post=1.5,
ITImodel = 'uniform',
ITImin = 0,
ITImax=1
)

POP = neurodesign.optimisation(
experiment=EXP,
weights=[0,0.5,0.25,0.25],
preruncycles = 100,
cycles = 100,
outdes = 10,
folder = "D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/",
optimisation='GA'
)
POP.optimise()


## random repeat of my stimuli list independantly for each stimuli (N repeatition depending of each initial list length to make 40 items)
## 3 different counter and go get next one in list when it's the stimuli turn in "order"




##need to see about rho, weights and preruncycles and cycles (and define how many design I need)



with open('D:/OneDrive/Documents/washU/projects/dataacquisition2021/JStasks/VWM/readingspan/designs/design_ME.txt','w') as f:
    f.write('var ITIs = [['+'],['.join([','.join([np.str(j) for j in i.ITI]) for i in POP.designs])+']];\n')
    f.write('var orders = [['+'],['.join([','.join([np.str(j) for j in i.order]) for i in POP.designs])+']];')
