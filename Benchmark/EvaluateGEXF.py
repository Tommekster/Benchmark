'''
Created on 29. 8. 2018

@author: Tomáš
'''

import networkx as nx
import os
from benchmark.evaluator import Evaluator

EVALUATION_FILE = 'output/evalGexf.txt'

def EvaluateGEXF():
    graphs = loadGraphs()
    for graph in graphs:
        G = getGraph(graph)
        original = getMemberships(G, 'community')
        evalJac = dict(
            bigClam=Evaluator(original,getMemberships(G, 'bigClam')).evaluate(),
            louvain=Evaluator(original,getMemberships(G, 'louvain')).evaluate(),
            olapSBMmax=Evaluator(original,getMemberships(G, 'olapSBMmax')).evaluate(), 
            olapSBM=Evaluator(original,getMemberships(G, 'olapSBM')).evaluate(),
            biSBM=Evaluator(original,getMemberships(G, 'biSBM')).evaluate()
            )
        evalFrc = dict(
            bigClam=Evaluator(original,getMemberships(G, 'bigClam')).evaluate(True),
            louvain=Evaluator(original,getMemberships(G, 'louvain')).evaluate(True),
            olapSBMmax=Evaluator(original,getMemberships(G, 'olapSBMmax')).evaluate(True), 
            olapSBM=Evaluator(original,getMemberships(G, 'olapSBM')).evaluate(True),
            biSBM=Evaluator(original,getMemberships(G, 'biSBM')).evaluate(True)
            )
        recordEvaluation(dict(graph=graph,evalJac=evalJac,evalFrc=evalFrc))

        
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
    EvaluateGEXF()
