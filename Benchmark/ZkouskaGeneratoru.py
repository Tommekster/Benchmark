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
    
    
def GrafBezPrekryvuIzolovane():
    ''' komunity jsou komponenty souvislosti: mu = 0 '''
    K = 3
    omega = np.eye(K, K)
    N = 100
    membership = [np.random.randint(K) for n in range(N)]
    G = np.array([[int(membership[n] == k) for n in range(N)] for k in range(K)])
    model = Model(G, omega)
    zadani = Zadani(model)
    generator = Generator(zadani)
    graf = generator()[0]
    nx.write_gexf(graf, 'bezPrekryvuIzolovane.gexf')

    
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
    zadani = Zadani(model)
    generator = Generator(zadani)
    for graf in generator(): break
    nx.write_gexf(graf, 'bezPreryvu.gexf')

    
def BipartitniGrafBezPrekryvu():
    model = VyrobBipartitniModel(100, np.array([[0, 1, 0], [1, 0, 1]]))
    zadani = Zadani(model)
    generator = BipartitniGenerator(zadani)
    graf = generator()[0]
    nx.write_gexf(graf, 'bipartitniBezPrekryvu.gexf')


if __name__ == '__main__':
    GrafBezPrekryvuIzolovane()
    GrafBezPrekryvu()
    BipartitniGrafBezPrekryvu()
