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

service = DetectionWebService()
EVALUATION_FILE = 'output/benchmark.txt'
GRAPHS_COUNT = 100

def Benchmark():
    graphName = 'GrafModelWithoutOverlaps'
    mu_params = {0, 0.01, 0.1, 0.2}
    for mu in mu_params:
        model = GrafModelWithoutOverlaps(mu)
        TestMethod(graphName, model, mu=mu)
        
def TestMethod(graphName, model, **kwargs):
    print('>{}\n\tParams:{}'.format(graphName, str(kwargs)))
    zadani = Zadani(model, GRAPHS_COUNT)
    for run, graph in enumerate(Generator(zadani)):
        print("\tProgress: {}/{}".format(run,GRAPHS_COUNT), end="\r", flush=True)
        
        olapSBMmax, olapSBM = service.olapSBM(graph)
        memberships = dict(
            bigClam=service.bigClam(graph),
            louvain=service.louvain(graph),
            olapSBMmax=olapSBMmax, olapSBM=olapSBM,
            biSBM=service.biSBM(graph)
        )
        
        evaluations = dict()
        for method in memberships:
            evaluations[method] = Evaluator(model.getMemberships(), memberships[method]).evaluate()
            
        record = dict(graph=graphName, params=kwargs, run=run, evaluations=evaluations)
        recordEvaluation(record)


def GrafModelWithoutOverlaps(mu=0.2):
    ''' Trochu propojene komunity: mu = 0.2 '''
    K = 3
    omega = np.array([[1 - mu, mu, 0], [mu, 1 - 2 * mu, mu], [0, mu, 1 - mu]])
    N = 100
    membership = [np.random.randint(K) for _ in range(N)]
    G = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(G, omega)
    return model

    
def clearEvaluationFile():
    with open('benchmark.txt', 'w') as _: pass

    
def recordEvaluation(record : dict):
    with open('benchmark.txt', 'a') as f: f.write('{}\n'.format(str(record)))


if __name__ == '__main__':
    Benchmark()
