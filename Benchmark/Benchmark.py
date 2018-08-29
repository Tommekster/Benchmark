'''
Created on 27. 8. 2018

@author: Tomáš
'''
import numpy as np
from benchmark.model import Model
from benchmark.zadani import Zadani
from benchmark.generator import Generator
from remoteService.detectionWebService import DetectionWebService
from benchmark.evaluator import Evaluator
from benchmark.modelBuilder import ModelBuilder
from benchmark.bipartitniModelBuilder import BipartitniModelBuilder

service = DetectionWebService()
EVALUATION_FILE = 'output/benchmark2.txt'
GRAPHS_COUNT = 100


def Benchmark():
    graphName = 'GraphModelWithoutOverlaps'
    mu_params = {0, 0.01, 0.1, 0.2}
    for mu in mu_params:
        model = GraphModelWithoutOverlaps(mu)
        TestMethod(graphName, model, mu=mu)
    graphName = 'GraphModelWithOverlaps'
    params = [((50, 50), 6), ((50, 50), 10), ((50, 50), 20), ((30, 60), 6), ((30, 60), 10)]
    for P in params:
        model = GraphModelWithOverlaps(P[0], P[1])
        TestMethod(graphName, model, sizes=P[0], common=P[1])
        
    TestMethod('BipartiteGraphWithoutOverlapsModel', BipartiteGraphWithoutOverlapsModel())
    TestMethod('TreeGraphModel', TreeGraphModel())
    
    params = [(0,0), (0,10), (0,16), (10,0), (10,10), (10,16), (20,0), (20,10), (20,16)]
    for P in params:
        model = BipartiteOverlappingGraphModel(P)
        TestMethod('BipartiteOverlappingGraphModel', model, common=P)
        
def TestMethod(graphName, model, **kwargs):
    print('>{}\n\tParams:{}'.format(graphName, str(kwargs)))
    zadani = Zadani(model, GRAPHS_COUNT)
    for run, graph in enumerate(Generator(zadani)):
        print("\tProgress: {}/{}".format(run, GRAPHS_COUNT), end="\r", flush=True)
        
        olapSBMmax, olapSBM = service.olapSBM(graph)
        memberships = dict(
            bigClam=service.bigClam(graph),
            louvain=service.louvain(graph),
            olapSBMmax=olapSBMmax, olapSBM=olapSBM,
            biSBM=service.biSBM(graph)
        )
        
        evaluations = dict()
        for method in memberships:
            evaluations[method] = Evaluator(model.getMemberships(), memberships[method]).evaluate(True)
            
        record = dict(graph=graphName, params=kwargs, run=run, evaluations=evaluations, frac=True)
        recordEvaluation(record)


def GraphModelWithoutOverlaps(mu=0.2):
    ''' Trochu propojene komunity: mu = 0.2 '''
    K = 3
    omega = np.array([[1 - mu, mu, 0], [mu, 1 - 2 * mu, mu], [0, mu, 1 - mu]])
    N = 100
    membership = [np.random.randint(K) for _ in range(N)]
    G = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(G, omega)
    return model


def GraphModelWithOverlaps(comSizes=(50, 50), commonNodes=20):
    N = sum(comSizes)
    A, B = comSizes
    C = int(commonNodes / 2)
    builder = ModelBuilder(N)
    builder.addCommunity(range(A + C)).addCommunity(range(N - B - C, N))
    model = builder.getModel()
    return model


def BipartiteGraphWithoutOverlapsModel():
    builder = BipartitniModelBuilder((60, 40))
    builder.addCommunityA(range(20))
    builder.addCommunityA(range(20, 40))
    builder.addCommunityA(range(40, 60))
    builder.addCommunityB(range(20))
    builder.addCommunityB(range(20, 40))
    builder.addCommunityRelation(0, 0)
    builder.addCommunityRelation(1, 1)
    builder.addCommunityRelation(2, 1)
    model = builder.getModel()
    return model


def TreeGraphModel():
    builder = BipartitniModelBuilder((80, 80))
    builder.addCommunityA(range(20))
    builder.addCommunityA(range(20, 40))
    builder.addCommunityA(range(40, 60))
    builder.addCommunityA(range(60, 80))
    builder.addCommunityB(range(20))
    builder.addCommunityB(range(20, 40))
    builder.addCommunityB(range(40, 60))
    builder.addCommunityB(range(60, 80))
    builder.addCommunityRelation(0, 0)
    builder.addCommunityRelation(0, 1)
    builder.addCommunityRelation(0, 2)
    builder.addCommunityRelation(1, 1)
    builder.addCommunityRelation(1, 3)
    builder.addCommunityRelation(2, 3)
    builder.addCommunityRelation(3, 3)
    model = builder.getModel()
    return model


def BipartiteOverlappingGraphModel(common=(10,10)):
    C = [int(c / 2) for c in common]
    builder = BipartitniModelBuilder((50, 90))
    builder.addCommunityA(range(25 + C[0]))
    builder.addCommunityA(range(25 - C[0], 50))
    builder.addCommunityB(range(30))
    builder.addCommunityB(range(30 - C[1], 60 + C[0]))
    builder.addCommunityB(range(60, 90))
    builder.addCommunityRelation(0, 0)
    builder.addCommunityRelation(0, 1)
    builder.addCommunityRelation(1, 1)
    builder.addCommunityRelation(1, 2)
    model = builder.getModel()
    return model

    
def clearEvaluationFile():
    with open(EVALUATION_FILE, 'w') as _: pass

    
def recordEvaluation(record : dict):
    with open(EVALUATION_FILE, 'a') as f: f.write('{}\n'.format(str(record)))


if __name__ == '__main__':
    Benchmark()
