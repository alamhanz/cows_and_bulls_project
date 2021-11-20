from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def bplot(params,axes = None, size = 1000):
    sample = np.random.beta(params[0], params[1], size=size)
    if axes is None :
        g1 = sns.distplot(sample)
    else:
        g1 = sns.histplot(sample, ax = axes)
    g1.set(ylabel=None)

    
def bplot_all(slots):
    part = int(np.ceil(len(slots)/2))
    f, axes = plt.subplots(2, part, figsize = (8,3))
    for p in slots:
        q = p-1
        i = (q//2)
        j = (q%2)
        bplot(slots[p], axes = axes[j][i], size = 8000)
        axes[j][i].set_title(str(p))

    plt.show()

class distpar:
    def __init__(self,number_param):
        self.n_params = number_param
        self.slots = dict()
        for i in range(self.n_params):
            self.slots[i+1] = (2,2)

    def bshows(self):
        bplot_all(self.slots)

    def update_beta(self,par,towards,steps = 1):
        if towards:
            a = self.slots[par][0]
            b = self.slots[par][1] + steps
        else:
            a = self.slots[par][0] + steps
            b = self.slots[par][1]
        self.slots[par] = (a,b)

    def update_slots(self,guess):
        ## update guess
        self.update_beta(guess,towards = True)
        
        ## update others
        for p in self.slots:
            if p!=guess:
                self.update_beta(p,towards = False) ## Kalo udah diupdate.. masa di update balik


