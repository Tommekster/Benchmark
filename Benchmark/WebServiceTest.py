'''
Created on 26. 8. 2018

@author: Tomáš
'''

import numpy as np
import networkx as nx
from benchmark.model import Model
from benchmark.generator import Generator
from remoteService.detectionWebService import DetectionWebService

def GrafWithoutOverlaps(mu = 0.2):
    ''' Trochu propojene komunity: mu = 0.2 '''
    K = 3 # number of communities
    omega = np.array([[1 - mu, mu, 0], [mu, 1 - 2 * mu, mu], [0, mu, 1 - mu]])
    N = 100 # number of nodes
    membership = [np.random.randint(K) for _ in range(N)]
    groupMatrix = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(groupMatrix, omega)
    generator = Generator(model)
    for graph in generator(): break
    return graph
    #nx.write_gexf(graf, output('bezPrekryvu.gexf'))
    
def appendMemberships(graph : nx.Graph, memberships, name = 'memberships'):
    communities = {n: str([c+1 for c, ms in enumerate(memberships) if n in ms]) for n in graph.nodes}
    nx.set_node_attributes(graph, communities, name)

if __name__ == '__main__':
    service = DetectionWebService()
    graph = GrafWithoutOverlaps()
    
    bigClam = service.bigClam(graph)
    louvain = service.louvain(graph)
    olapSBMmax, olapSBM = service.olapSBM(graph,10,10)
    
    appendMemberships(graph, bigClam, 'bigCLAM')
    appendMemberships(graph, louvain, 'louvain')
    appendMemberships(graph, olapSBM, 'olapSBM')
    appendMemberships(graph, olapSBMmax, 'olapSBMmax')
    
    nx.write_gexf(graph, 'output/serviceTest.gexf')