'''
Created on 5. 6. 2018

@author: Tom
'''
import numpy as np
import model
from powerLaw import powerLaw


def VyrobBipartitniZadani(N, C : np.ndarray, alpha=2.1, mu=2):
    """
    Parametry:
    N : pocet vrcholu
    C : matice propojeni komunit rozmeru kA x kB
        kA : pocet komunit typu A 
        kB : pocet komunit typu B
    alpha : powerlaw koeficient pro stupen vrcholu
    mu : mixing parameter (unused)
    """
    kA, kB = C.shape
    k = kA + kB
    
    M = __vyrobClenstvi(N, kA, kB)
    T = __typVrcholu(M, kA, kB)
    D = __vahaStupneVrcholu(N, alpha)
    G = __maticeAffiliaci(k, D)
    
    
def __vyrobClenstvi(N, kA, kB):
    assert(N > 0 and kA > 0 and kB > 0)
    
    # maximalni clenstvi vrcholu v komunite
    MM = [np.random.randint(kA + kB) for i in range(N)]
    
    # usporadat clenstvi, aby byly nejprve typu A a pak typu B
    M = [m for m in MM if m < kA]
    M.extend([m for m in MM if not m < kA])
        
    return M


def __typVrcholu(M, kA, kB):
    return [int(not m < kA) for m in M]


def __vahaStupneVrcholu(N, alpha):
    return [powerLaw(alpha) for i in range(N)]


def __maticeAffiliaci(numComs, nodeWeights):
    G = [[w if c == com else 0 for w, c in zip(nodeWeights, com)] for com in range(numComs)]
