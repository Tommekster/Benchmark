'''
Created on 26. 8. 2018

@author: Tomáš
'''

from benchmark import Model, Generator, BipartitniGenerator, Evaluator, BipartitniModelBuilder
import networkx as nx
import numpy as np
from remoteService import DetectionWebService


def GrafWithoutOverlaps(mu=0.2):
    ''' Trochu propojene komunity: mu = 0.2 '''
    K = 3  # number of communities
    omega = np.array([[1 - mu, mu, 0], [mu, 1 - 2 * mu, mu], [0, mu, 1 - mu]])
    N = 100  # number of nodes
    membership = [np.random.randint(K) for _ in range(N)]
    groupMatrix = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(groupMatrix, omega)
    generator = Generator(model)
    for graph in generator(): break
    return graph, model


def BipartiteGraphWithoutOverlaps():
    builder = BipartitniModelBuilder((60,40))
    builder.addCommunityA(range(20))
    builder.addCommunityA(range(20, 40))
    builder.addCommunityA(range(40, 60))
    builder.addCommunityB(range(20))
    builder.addCommunityB(range(20,40))
    builder.addCommunityRelation(1, 0)
    builder.addCommunityRelation(0, 1)
    builder.addCommunityRelation(2, 1)
    model = builder.getModel()
    # model = VyrobBipartitniModel(100, np.array([[0, 1, 0], [1, 0, 1]]))
    generator = BipartitniGenerator(model)
    graf = generator()[0]
    return graf, model
    # nx.write_gexf(graf, output('bipartitniBezPrekryvu.gexf'))

    
def appendMemberships(graph : nx.Graph, memberships, name='memberships'):
    communities = {n: str([c + 1 for c, ms in enumerate(memberships) if n in ms]) for n in graph.nodes}
    nx.set_node_attributes(graph, communities, name)


if __name__ == '__main__':
    service = DetectionWebService()
    #graph, model = GrafWithoutOverlaps()
    graph, model = BipartiteGraphWithoutOverlaps()
    
    #bigClam = service.bigClam(graph)
    # louvain = service.louvain(graph)
    # olapSBMmax, olapSBM = service.olapSBM(graph,10,10)
    biSBM = service.biSBM(graph)
    
    evaluator = Evaluator(model.getMemberships(), biSBM)
    evaluation = evaluator.evaluate()
    print(evaluation)
    
    # appendMemberships(graph, bigClam, 'bigCLAM')
    # appendMemberships(graph, louvain, 'louvain')
    # appendMemberships(graph, olapSBM, 'olapSBM')
    # appendMemberships(graph, olapSBMmax, 'olapSBMmax')
    appendMemberships(graph, biSBM, 'biSBM')
    
    nx.write_gexf(graph, 'output/serviceTest.gexf')
    
