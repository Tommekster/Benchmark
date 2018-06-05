'''
Created on 4. 6. 2018

@author: Tom
'''
from Zadani import Zadani, BipartitniZadani

class Generator(object):
    '''
    classdocs
    '''


    def __init__(self, zadani : Zadani):
        '''
        Constructor
        '''
        self.zadani = zadani
        
class BipartitniGenerator(Generator):
    
    def __init__(self, zadani : BipartitniZadani):
        super().__init__(zadani)
        
        