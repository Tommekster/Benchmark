'''
Created on 5. 6. 2018

@author: Tom
'''
import numpy as np

class Model(object):
    '''
    classdocs
    '''


    def __init__(self, G : np.ndarray, omega : np.ndarray):
        '''
        Constructor
        '''
        assert(np.min(G) >= 0)
        assert(np.min(omega) >= 0 and np.max(omega) <= 1)
        
        self.G = G 
        self.omega = omega 
        
        self.__LoadNumsFromMatrix(G)
        
    def __LoadNumsFromMatrix(self, G : np.ndarray):
        self.numComs, self.numNodes = self.G.shape
        
class BipartitniModel(Model):
    def __init__(self, A : np.ndarray, B : np.ndarray, C : np.ndarray):
        '''
        Parametry:
        A: matice rozmeru kA x nA (pocet komunit x pocet uzlu typu A)
        B: matice rozmeru kB x nB (pocet komunit x pocet uzlu typu B)
        C: matice rozmeru kA x kB
        '''
        
        assert(np.min(A) >= 0 and np.min(B) >= 0)
        assert(np.min(C) >= 0 and np.max(C) <= 1)
        
        self.A = A
        self.B = B 
        self.C = C 
        
        G, omega = self.ConvertModel(A, B, C)
        super().__init__(G, omega)
        
        self.__LoadNumsFromMatrices(A, B)
        
    def ConvertModel(self, A : np.ndarray, B : np.ndarray, C : np.ndarray):
        '''
        Prevede bipartitni model A,B,C na obecny G a omega
        '''
        kA, nA = A.shape
        kB, nB = B.shape
        assert(C.shape[0] == kA & C.shape[1] == kB)
        
        G = np.zeros((kA + kB, nA + nB))
        G[0:kA, 0:nA] = A
        G[kA:(kA + kB), nA:(nA + nB)] = B
        
        omega = np.zeros((kA + kB, kA + kB))
        omega[0:kA, kA:(kA + kB)] = C
        omega[kA:(kA + kB), 0:kA] = C.transpose()
        
        return G, omega
    
    def __LoadNumsFromMatrices(self,  A : np.ndarray, B : np.ndarray):
        self.numComsTypeA, self.numNodesTypeA = A.shape
        self.numComsTypeB, self.numNodesTypeB = B.shape
