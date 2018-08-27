'''
Created on 4. 6. 2018

@author: Tom
'''

import os.path

from benchmark.bipartitniModelBuilder import BipartitniModelBuilder
from benchmark.bipartitniModelCreator import VyrobBipartitniModel
from benchmark.generator import Generator
from benchmark.model import Model
from benchmark.modelBuilder import ModelBuilder
from benchmark.zadani import Zadani
import networkx as nx
import numpy as np
from remoteService.detectionWebService import DetectionWebService
from benchmark.evaluator import Evaluator


def GrafBezPrekryvuIzolovane():
    ''' komunity jsou komponenty souvislosti: mu = 0 '''
    K = 3
    omega = np.eye(K, K)
    N = 100
    membership = [np.random.randint(K) for _ in range(N)]
    G = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(G, omega)
    generateDetectAndSave(model, 'bezPrekryvuIzolovane.gexf')


def GrafWithoutOverlaps(mu=0.2):
    ''' Trochu propojene komunity: mu = 0.2 '''
    K = 3
    omega = np.array([[1 - mu, mu, 0], [mu, 1 - 2 * mu, mu], [0, mu, 1 - mu]])
    N = 100
    membership = [np.random.randint(K) for _ in range(N)]
    G = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(G, omega)
    generateDetectAndSave(model, 'bezPrekryvu.gexf')


def GrafSPrekryvem():
    N = 100
    builder = ModelBuilder(N)  # .addCommunities(3, range(N))
    builder.addCommunity(range(70)).addCommunity(range(30, 100))
    model = builder.getModel()
    generateDetectAndSave(model, 'sPrekryvem.gexf')


def GrafSVolnymiVrcholy():
    N = 100
    mb = ModelBuilder(N)  # .addCommunities(3, range(N))
    mb.addCommunity(range(40)).addCommunity(range(60, 100))
    model = mb.getModel()
    generateDetectAndSave(model, 'sVolnymi.gexf')


def BipartitniGrafBezPrekryvu():
    model = VyrobBipartitniModel(100, np.array([[0, 1, 0], [1, 0, 1]]))
    generateDetectAndSave(model, 'bipartitniBezPrekryvu.gexf')


def BipartitniGrafSPrekryvem():
    builder = BipartitniModelBuilder((50, 50))
    builder.addCommunityA(range(30))
    builder.addCommunityA(range(20, 50))
    builder.addCommunityB(range(20))
    builder.addCommunityB(range(15, 35))
    builder.addCommunityB(range(30, 50))
    builder.addCommunityRelation(0, 0)
    builder.addCommunityRelation(0, 1)
    builder.addCommunityRelation(1, 1)
    builder.addCommunityRelation(1, 2)
    model = builder.getModel()
    generateDetectAndSave(model, 'bipartitniSPrekryvem.gexf')


service = DetectionWebService()

    
def generateDetectAndSave(model : Model, fileName):
    graph = Generator(model).next()
    
    olapSBMmax, olapSBM = service.olapSBM(graph, 6, 50)
    memberships = dict(
        bigClam=service.bigClam(graph),
        louvain=service.louvain(graph),
        olapSBMmax=olapSBMmax, olapSBM=olapSBM,
        biSBM=service.biSBM(graph)
    )
    
    evaluations = dict()
    for method in memberships:
        appendMemberships(graph, memberships[method], method)
        evaluations[method] = Evaluator(model.getMemberships(), memberships[method]).evaluate()
        
    record = dict(graph=fileName, evaluations=evaluations)
    recordEvaluation(record)
    
    nx.write_gexf(graph, output(fileName))

    
def clearEvaluationFile():
    with open(output('evaluation.txt'), 'w') as _: pass

    
def recordEvaluation(record : dict):
    with open(output('evaluation.txt'), 'a') as f: f.write('{}\n'.format(str(record)))

            
def output(filename):
    return os.path.join('output', filename)

    
def appendMemberships(graph : nx.Graph, memberships, name='memberships'):
    communities = {n: str([c + 1 for c, ms in enumerate(memberships) if n in ms]) for n in graph.nodes}
    nx.set_node_attributes(graph, communities, name)


if __name__ == '__main__':
    GrafBezPrekryvuIzolovane()
    GrafWithoutOverlaps()
    GrafSPrekryvem()
    GrafSVolnymiVrcholy()
    BipartitniGrafBezPrekryvu()
    BipartitniGrafSPrekryvem()
