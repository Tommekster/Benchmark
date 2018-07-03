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
        graph = self.__generuj(weights)
        comsLabels = self.__getCommunityLabels()
        nx.set_node_attributes(graph, comsLabels, 'community')
        return graph
        
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
    
    def __getCommunityLabels(self):
        coms = {}
        for n in range(self.zadani.model.get_num_nodes()):
            coms[n+1]=str(self.zadani.model.getCommunities(n))
        return coms
    
        
class BipartitniGenerator(Generator):
    
    def __init__(self, zadani : BipartitniZadani):
        super().__init__(zadani)
        
    def generate(self) -> nx.Graph:
        G = Generator.generate(self)
        positions = self.__getNodePositions()
        nx.set_node_attributes(G,positions,'viz')
        return G
    
    def __getNodePositions(self):
        viz = {}
        nums = [0,0]
        for n in range(self.zadani.model.get_num_nodes()):
            t = self.zadani.model.GetNodeType(n)
            viz[n+1] = {'position':{'x':nums[t]*10.0,'y':1000.0*t}}
            nums[t] += 1
        return viz