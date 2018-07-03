'''
Created on 4. 6. 2018

@author: Tom
'''
from benchmark.zadani import Zadani
from benchmark.model import Model
import numpy as np
import networkx as nx


class Generator(object):
    '''
    classdocs
    '''

    def __init__(self, zadaniNeboModel):
        '''
        Constructor
        '''
        if type(zadaniNeboModel) == Zadani:
            self.zadani = zadaniNeboModel
        elif type(zadaniNeboModel) == Model:
            self.zadani = Zadani(zadaniNeboModel, count=1)
        else: raise NotImplementedError()
        
    def __call__(self) -> nx.Graph:
        for model in self.zadani.getModels():
            yield self.generate(model)
        
    def generate(self, model):
        weights = self.__vyrobVahy(model)
        graph = self.__generuj(weights)
        comsLabels = self.__getCommunityLabels(model)
        nx.set_node_attributes(graph, comsLabels, 'community')
        return graph
        
    def __vyrobVahy(self, model):
        groups = model.G
        behavior = model.omega
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
    
    def __getCommunityLabels(self, model):
        coms = {}
        for n in range(model.get_num_nodes()):
            coms[n + 1] = str(model.getCommunities(n))
        return coms
    
        
class BipartitniGenerator(Generator):
    
    def __init__(self, zadaniNeboModel):
        super().__init__(zadaniNeboModel)
        
    def generate(self, model) -> nx.Graph:
        G = Generator.generate(self, model)
        positions = self.__getNodePositions(model)
        nx.set_node_attributes(G, positions, 'viz')
        return G
    
    def __getNodePositions(self, model):
        viz = {}
        nums = [0, 0]
        for n in range(model.get_num_nodes()):
            t = model.GetNodeType(n)
            viz[n + 1] = {'position':{'x':nums[t] * 10.0, 'y':1000.0 * t}}
            nums[t] += 1
        return viz
