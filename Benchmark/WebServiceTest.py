'''
Created on 26. 8. 2018

@author: Tomáš
'''

import numpy as np
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

if __name__ == '__main__':
    service = DetectionWebService()
    graph = GrafWithoutOverlaps()
    memberships = service.louvain(graph)
    print(memberships)