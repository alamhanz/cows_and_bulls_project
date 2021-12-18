from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

def bplot(params,axes = None, size = 1000):
    sample = np.random.beta(params[0], params[1], size = size)
    if axes is None :
        g1 = sns.distplot(sample)
    else:
        g1 = sns.histplot(sample, ax = axes)
    g1.set(ylabel=None)

    
def bplot_all(slots):
    part = int(np.ceil(len(slots)/2))
    f, axes = plt.subplots(2, part, figsize = (8,3))
    for q0 in slots:
        q = int(q0)
        # q = p-1
        i = (q//2)
        j = (q%2)
        bplot(slots[q0], axes = axes[j][i], size = 8000)
        axes[j][i].set_title(str(q))

    plt.show()

def beta_stats(a,b):
    desc = beta.stats(a, b, moments='mvsk')
    desc = [float(i) for i in desc]
    bstat = dict(zip(['mean','var','skew','kurt'],desc))
    return bstat

class distpar:
    def __init__(self,lower_bound = 0.2):
        self.slots = dict()
        self.stats = dict()
        self.lbound = lower_bound
        self.lbound_pos = lower_bound ## --> ideally it has different value with lbound
        self.possible_bulls = []
        ## 10 digits
        for i in range(10):
            self.slots[str(i)] = (2,2)
            dstats = beta_stats(2,2)
            self.stats[str(i)] = dstats
            self.possible_bulls.append(str(i))

    def bshows(self):
        bplot_all(self.slots)

    def update_beta(self,guess,towards,steps = 1):
        for par in guess:
            if towards:
                a = self.slots[par][0] + steps
                b = self.slots[par][1] 
            else:
                a = self.slots[par][0] 
                b = self.slots[par][1] + steps
            self.slots[par] = (a,b)
            self.stats[par] = beta_stats(a,b)

    def update_slots(self,guess):
        ## update the guess
        self.update_beta(guess,towards = False, steps = 50) 
        
        ## update the others
        for p in self.slots:
            if p not in guess and self.stats[p]['mean']>self.lbound:
                self.update_beta(p,towards = True,steps = 1)

        self.possible_bulls = [i for i in self.possible_bulls if self.stats[i]['mean']>self.lbound_pos]

    def make_guess(self):
        x = random.choice(self.possible_bulls)
        print('try ', x)
        return x

## Notes:
## more steps towards false where the probability approach 0
## more steps towards true where the probability approach 1
## the towards true steps really impacting the towards false steps in the end (must have large steps towards false if its really impossible)
## Lbound is a lower bound value where the number beta is not update anymore
## Lbound_pos is a lower bound to become possible number
## steps is depend on digits and on which stage