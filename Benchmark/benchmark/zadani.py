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

        
class BipartitniZadani(Zadani):
    
    def __init__(self, model : BipartitniModel, count : int=1):
        
        Zadani.__init__(self,model, count)
