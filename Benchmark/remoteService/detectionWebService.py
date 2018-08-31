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
        
    def bigClam(self, graph : nx.Graph, comsNum=-1):
        if not comsNum: comsNum = -1
        edges = self._getEdges(graph)
        partitions = self.proxy.bigClam(edges, comsNum)
        return self._bipartitePartitions(graph, partitions)
    
    def louvain(self, graph : nx.Graph):
        edges = self._getEdges(graph)
        nodes = self._getNodes(graph)
        partitions = self.proxy.louvain(nodes, edges)
        return self._bipartitePartitions(graph, partitions)
    
    def olapSBM(self, graph : nx.Graph, maxComs=10, runsPerNetwork=10):
        if not maxComs: maxComs = 10
        edges = self._getEdges(graph)
        multiplePartitions = self.proxy.olapSBM(edges, maxComs, runsPerNetwork)
        return tuple([self._bipartitePartitions(graph, partitions) for partitions in multiplePartitions])
    
    def biSBM(self, graph : nx.Graph, Ka=5, Kb=5, isDegreeCorrected=True, KLsteps=5):
        if not Ka or not Kb: Ka, Kb = 5, 5
        edges = self._getEdges(graph)
        types = self._getTypes(graph)
        partitions = self.proxy.biSBM(edges, types, Ka, Kb, isDegreeCorrected, KLsteps)
        return self._bipartitePartitions(graph, partitions)
    
    def _getEdges(self, graph : nx.Graph):
        return list(graph.edges)
    
    def _getNodes(self, graph : nx.Graph):
        return list(graph.nodes)
    
    def _getTypes(self, graph: nx.Graph):
        types = list(self.__generateTypes(graph))
        types.sort(key=lambda T: T[0])
        return [T[1] for T in types]
    
    def __generateTypes(self, graph):
        for n in graph.nodes:
            node = graph.node[n]
            yield [int(n), node['type'] + 1 if 'type' in node else 1]
            
    def _bipartitePartitions(self, graph:nx.Graph, partitions):
        typeSets = self.__nodeTypeSets(graph)
        return [list(typeSet & set(P)) for P in partitions for typeSet in typeSets]
    
    def __nodeTypeSets(self, graph):
        types = self._getTypes(graph)
        return [set([n + 1 for n, t in enumerate(types) if t == T]) for T in (1, 2)]
