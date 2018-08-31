'''
Created on 31. 8. 2018

@author: Tomáš
'''
import numpy as np
import matplotlib.pyplot as plt
from benchmark.zadani import Zadani
from benchmark.generator import Generator
from benchmark.model import Model
from benchmark.bipartitniModelBuilder import BipartitniModelBuilder
from benchmark.modelBuilder import ModelBuilder

EVALUATION_FILE = 'output/degreeDistribution.txt'
OUTPUT_FOLDER = 'output/degrees/'
GRAPHS_COUNT = 100


def DigreeDistribution():
    pass
    graphName = 'GraphModelWithoutOverlaps'
    mu_params = {0, 0.01, 0.1, 0.2}
    for mu in mu_params:
        model = GraphModelWithoutOverlaps(mu)
        plotDegreeDistribution(graphName, model, mu=mu)
    graphName = 'GraphModelWithOverlaps'
    params = [((50, 50), 6), ((50, 50), 10), ((50, 50), 20), ((30, 60), 6), ((30, 60), 10)]
    for P in params:
        model = GraphModelWithOverlaps(P[0], P[1])
        plotDegreeDistribution(graphName, model, sizes=P[0], common=P[1])
        
    plotDegreeDistribution('BipartiteGraphWithoutOverlapsModel', BipartiteGraphWithoutOverlapsModel())
    plotDegreeDistribution('TreeGraphModel', TreeGraphModel())
    
    params = [(0, 0), (0, 10), (0, 16), (10, 0), (10, 10), (10, 16), (20, 0), (20, 10), (20, 16)]
    for P in params:
        model = BipartiteOverlappingGraphModel(P)
        plotDegreeDistribution('BipartiteOverlappingGraphModel', model, common=P)

        
def plotDegreeDistribution(graphName, model, **kwargs):
    print('>{}\n\tParams:{}'.format(graphName, str(kwargs)))
    zadani = Zadani(model, GRAPHS_COUNT)
    degrees = []
    for run, graph in enumerate(Generator(zadani)):
        print("\tProgress: {}/{}\t{}".format(run, GRAPHS_COUNT, graphName), end="\r", flush=True)
        degrees += [D[1] for D in graph.degree()]
    plotDistribution(degrees, graphName, kwargs, GRAPHS_COUNT)
    
def plotDistribution(_degrees, graphName, params, count):
    degrees = np.array(_degrees)
#     maxDegree = np.max(degrees)
#     x = np.arange(maxDegree+1)
#     y = np.array([np.sum(degrees < d)/count for d in x])
    plt.hist(degrees, bins=99)
    plt.title('{}'.format(params))
    plt.savefig('{}{}_{}.png'.format(OUTPUT_FOLDER,graphName,str(params).__hash__()))
    plt.close()

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


def BipartiteOverlappingGraphModel(common=(10, 10)):
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
    DigreeDistribution()
