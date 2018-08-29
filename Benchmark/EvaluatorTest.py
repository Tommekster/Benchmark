'''
Created on 26. 8. 2018

@author: Tomáš
'''

from benchmark import Model, Generator, Evaluator
import networkx as nx
import numpy as np
from remoteService import DetectionWebService
from EvaluateGEXF import getMemberships


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

    
def appendMemberships(graph : nx.Graph, memberships, name='memberships'):
    communities = {n: str([c + 1 for c, ms in enumerate(memberships) if n in ms]) for n in graph.nodes}
    nx.set_node_attributes(graph, communities, name)


if __name__ == '__main__':
    print('Packages loaded')
    service = DetectionWebService()
    #graph, model = GrafWithoutOverlaps()
    graph = nx.read_gexf('output/bezPrekryvu.gexf')
    nx.write_gexf(graph, 'output/evaluatorTest.gexf')
    
    memberships = getMemberships(graph, 'community')
    olapSBM = getMemberships(graph, 'olapSBM')
    
    selfEvaluator = Evaluator(memberships, memberships)
    selfEvaluation = selfEvaluator.evaluate()
    print(selfEvaluation)
    with open('output/WOO.self.eval.txt','w') as f: f.write(str(selfEvaluation)+'\n')
    
    evaluator = Evaluator(memberships, olapSBM)
    evaluation = evaluator.evaluate()
    print(evaluation)
    with open('output/WOO.oSBM.eval.txt','w') as f: f.write(str(evaluation)+'\n')
    evaluator.plot.comparison('output/WOO.oSBM.cmp.jac.png')
    evaluator.plot.comparison('output/WOO.oSBM.cmp.frc.png',True)
    evaluator.plot.aggregated('output/WOO.oSBM.agr.jac.png')
    evaluator.plot.aggregated('output/WOO.oSBM.agr.frc.png',True)
    evaluator.plot.selfAggregated('output/WOO.oSBM.sagr.jac.png')
    evaluator.plot.selfAggregated('output/WOO.oSBM.sagr.frc.png',True)
    evaluator.plot.selfOriginal('output/WOO.oSBM.sorg.jac.png')
    evaluator.plot.selfOriginal('output/WOO.oSBM.sorg.frc.png',True)
    evaluator.plot.selfDetected('output/WOO.oSBM.sdet.jac.png')
    evaluator.plot.selfDetected('output/WOO.oSBM.sdet.frc.png',True)
    
