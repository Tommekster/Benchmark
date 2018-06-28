'''
Created on 4. 6. 2018

@author: Tom
'''
from benchmark.zadani import Zadani, BipartitniZadani
import numpy as np
import networkx as nx


class Generator(object):
    '''
    classdocs
    '''

    def __init__(self, zadani : Zadani):
        '''
        Constructor
        '''
        self.zadani = zadani
        
    def __call__(self) -> nx.Graph:
        return self.generate()
        
    def generate(self):
        weights = self.__vyrobVahy()
        return self.__generuj(weights)
        
    def __vyrobVahy(self):
        groups = self.zadani.model.G
        behavior = self.zadani.model.omega
        return groups.transpose().dot(behavior).dot(groups)
    
    def __generuj(self, weights : np.array) -> nx.Graph:
        G = nx.Graph()
        N, NN = weights.shape
        for i in range(N):
            G.add_node(i + 1, node_index=i)
        for i in range(N):
            for j in range(i + 1, N):
                if np.random.rand() < 1 - np.exp(-weights[i, j]):
                    G.add_edge(i + 1, j + 1)
        return G
    
        
class BipartitniGenerator(Generator):
    
    def __init__(self, zadani : BipartitniZadani):
        super().__init__(zadani)
        
    def generate(self) -> nx.Graph:
        G = Generator.generate(self)
        for n in G.nodes:
            print(n)
        return G