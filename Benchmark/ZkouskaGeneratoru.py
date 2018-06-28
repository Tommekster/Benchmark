'''
Created on 4. 6. 2018

@author: Tom
'''

from benchmark.bipartitniModelCreator import VyrobBipartitniModel
from benchmark.zadani import BipartitniZadani
from benchmark.generator import BipartitniGenerator
import numpy as np
import networkx as nx

if __name__ == '__main__':
    model = VyrobBipartitniModel(10, np.array([[0, 1, 0], [1, 0, 1]]))
    zadani = BipartitniZadani(model)
    generator = BipartitniGenerator(zadani)
    graf = generator()
    nx.write_gexf(graf, 'zkouskaGrafu.gexf')