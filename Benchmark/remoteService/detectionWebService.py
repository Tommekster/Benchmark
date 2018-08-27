'''
Created on 26. 8. 2018

@author: Tomáš
'''

import networkx as nx
from .serviceProxy import ServiceProxy


class DetectionWebService(object):
    '''
    classdocs
    '''

    def __init__(self, url="http://localhost:8100/jsonrpc"):
        '''
        Constructor
        '''
        self.proxy = ServiceProxy(url)
        
    def bigClam(self, graph : nx.Graph):
        edges = self._getEdges(graph)
        return self.proxy.bigClam(edges)
    
    def louvain(self, graph : nx.Graph):
        edges = self._getEdges(graph)
        nodes = self._getNodes(graph)
        return self.proxy.louvain(nodes, edges)
    
    def olapSBM(self, graph : nx.Graph, maxComs=10, runsPerNetwork=20):
        edges = self._getEdges(graph)
        return self.proxy.olapSBM(edges, maxComs, runsPerNetwork)
    
    def biSBM(self, graph : nx.Graph, Ka=5, Kb=5, isDegreeCorrected=True, KLsteps=5):
        edges = self._getEdges(graph)
        types = self._getTypes(graph)
        return self.proxy.biSBM(edges, types, Ka, Kb, isDegreeCorrected, KLsteps)
    
    def _getEdges(self, graph : nx.Graph):
        return list(graph.edges)
    
    def _getNodes(self, graph : nx.Graph):
        return list(graph.nodes)
    
    def _getTypes(self, graph: nx.Graph):
        return list(self.__generateTypes(graph))
    
    def __generateTypes(self, graph):
        for n in graph.nodes:
            node = graph.node[n]
            yield node['type'] + 1 if 'type' in node else 1
