'''
Created on 4. 6. 2018

@author: Tom
'''
from benchmark.model import Model, BipartitniModel


class Zadani(object):
    '''
    Obsahuje model jako zadani pro generator grafu
    '''

    def __init__(self, model : Model, count : int=1):
        '''
        Constructor
        '''
        self.model = model
        self.count = count
        
    def getModels(self):
        for cnt in range(self.count):
            yield self.model