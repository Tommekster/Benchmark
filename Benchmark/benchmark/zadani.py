'''
Created on 4. 6. 2018

@author: Tom
'''
from benchmark.model import Model, BipartitniModel


class Zadani(object):
    '''
    Obsahuje model jako zadani pro generator grafu
    '''

    def __init__(self, model : Model):
        '''
        Constructor
        '''
        self.model = model

        
class BipartitniZadani(Zadani):
    
    def __init__(self, model : BipartitniModel):
        
        super().__init__(model)
