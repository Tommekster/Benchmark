'''
Created on 29. 8. 2018

@author: Tomáš
'''

import networkx as nx
import os
from benchmark.evaluator import Evaluator
from remoteService.detectionWebService import DetectionWebService

EVALUATION_FILE = 'output/evalGexf.txt'
service = DetectionWebService("http://localhost:8101/jsonrpc")


def EvaluateGEXF(useService=False):
    graphs = loadGraphs()
    for graph in graphs:
        G = getGraph(graph)
        if useService:
            memberships = detectMemberships(G)
        else:
            memberships = membershipsFromGEXF(G)
        original = getMemberships(G, 'community')
        evalFrc = evaluateMethods(original, memberships, True)
        recordEvaluation(dict(graph=graph, evaluation=evalFrc))

        
def detectMemberships(graph:nx.Graph):
    comsNum = None
    comsBiNum = (None, None)
            
    olapSBMmax, olapSBM = service.olapSBM(graph, comsNum)
    memberships = dict(
        louvain=service.louvain(graph),
        olapSBMmax=olapSBMmax, olapSBM=olapSBM,
        bigClam=service.bigClam(graph, comsNum),
        biSBM=service.biSBM(graph, comsBiNum[0], comsBiNum[1])
    )
    return memberships


def membershipsFromGEXF(G:nx.Graph, methods=['community', 'louvain', 'olapSBMmax', 'olapSBM', 'bigClam', 'biSBM']):
    return {method: getMemberships(G, method) for method in methods}

        
def evaluateMethods(original, memberships, useFraction=True):
    return {method: Evaluator(original, memberships[method]).evaluate(useFraction) for method in memberships}

        
def getMemberships(G, attribute):
    communities = {n: eval(G.node[n][attribute]) for n in G.nodes}
    maxCom = max([c for n in communities for c in communities[n]])
    memberships = [[n for n in communities if c in communities[n]] for c in range(maxCom + 1)]
    memberships = [M for M in memberships if len(M) > 0]
    return memberships
        
        
def getGraph(graph):
    return nx.read_gexf('output/{}.gexf'.format(graph))


def loadGraphs():
    graphs = [f.name.replace('.gexf', '') for f in os.scandir('output') if f.name.endswith('.gexf')]
    return graphs

    
def clearEvaluationFile():
    with open(EVALUATION_FILE, 'w') as _: pass

    
def recordEvaluation(record : dict):
    with open(EVALUATION_FILE, 'a') as f: f.write('{}\n'.format(str(record)))


if __name__ == '__main__':
    EvaluateGEXF(True)
