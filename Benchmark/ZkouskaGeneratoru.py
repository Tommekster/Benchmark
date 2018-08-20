'''
Created on 4. 6. 2018

@author: Tom
'''

from benchmark.bipartitniModelCreator import VyrobBipartitniModel
from benchmark.zadani import Zadani
from benchmark.model import Model
from benchmark.generator import BipartitniGenerator, Generator
import numpy as np
import networkx as nx
from benchmark.modelBuilder import ModelBuilder
from benchmark.bipartitniModelBuilder import BipartitniModelBuilder
import os.path


def GrafBezPrekryvuIzolovane():
    ''' komunity jsou komponenty souvislosti: mu = 0 '''
    K = 3
    omega = np.eye(K, K)
    N = 100
    membership = [np.random.randint(K) for n in range(N)]
    G = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(G, omega)
    saveMembers(model, output('coms.bezPrekryvuIzolovane.txt'))
    zadani = Zadani(model)
    generator = Generator(zadani)
    graf = generator()[0]
    nx.write_gexf(graf, output('bezPrekryvuIzolovane.gexf'))


def GrafBezPrekryvu():
    ''' Trochu propojene komunity: mu = 0.2 '''
    mu = 0.2
    K = 3
    omega = np.eye(K, K)
    omega = np.array([[1 - mu, mu, 0], [mu, 1 - 2 * mu, mu], [0, mu, 1 - mu]])
    N = 100
    membership = [np.random.randint(K) for n in range(N)]
    G = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(G, omega)
    saveMembers(model, output('coms.bezPrekryvu.txt'))
    zadani = Zadani(model)
    generator = Generator(zadani)
    for graf in generator(): break
    nx.write_gexf(graf, output('bezPrekryvu.gexf'))


def GrafSPrekryvem():
    N = 100
    mb = ModelBuilder(N)  # .addCommunities(3, range(N))
    mb.addCommunity(range(70)).addCommunity(range(30, 100))
    model = mb.getModel()
    saveMembers(model, output('coms.sPrekryvem.txt'))
    generator = Generator(model)
    for graf in generator(): break
    nx.write_gexf(graf, output('sPrekryvem.gexf'))


def GrafSVolnymiVrcholy():
    N = 100
    mb = ModelBuilder(N)  # .addCommunities(3, range(N))
    mb.addCommunity(range(40)).addCommunity(range(60, 100))
    model = mb.getModel()
    saveMembers(model, output('coms.sVolnymi.txt'))
    generator = Generator(model)
    for graf in generator(): break
    nx.write_gexf(graf, output('sVolnymi.gexf'))


def BipartitniGrafBezPrekryvu():
    model = VyrobBipartitniModel(100, np.array([[0, 1, 0], [1, 0, 1]]))
    saveMembers(model, output('coms.bipartitniBezPrekryvu.txt'))
    zadani = Zadani(model)
    generator = BipartitniGenerator(zadani)
    graf = generator()[0]
    nx.write_gexf(graf, output('bipartitniBezPrekryvu.gexf'))


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
    saveMembers(model, output('coms.bipartitniSPrekryvem.txt'))
    zadani = Zadani(model)
    generator = BipartitniGenerator(zadani)
    graf = generator()[0]
    nx.write_gexf(graf, output('bipartitniSPrekryvem.gexf'))

def saveMembers(model: Model, filename):
    coms = model.get_num_coms()
    with open(filename,'w') as f:
        for c in range(coms):
            f.write('\t'.join([str(n+1) for n in model.getMembers(c)])+'\n')
            
def output(filename):
    return os.path.join('output',filename)

if __name__ == '__main__':
    pass
    GrafBezPrekryvuIzolovane()
    GrafBezPrekryvu()
    GrafSPrekryvem()
    GrafSVolnymiVrcholy()
    BipartitniGrafBezPrekryvu()
    BipartitniGrafSPrekryvem()
