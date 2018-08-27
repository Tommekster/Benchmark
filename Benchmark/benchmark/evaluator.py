'''
Created on 26. 8. 2018

@author: Tomáš
'''

from benchmark.membershipList import MembershipsList
import numpy as np
from builtins import callable


class Evaluator(object):
    '''
    classdocs
    '''

    def __init__(self, original : MembershipsList, detected : MembershipsList):
        '''
        Constructor
        '''
        self.__original = original if isinstance(original, MembershipsList) else MembershipsList(original)
        self.__detected = detected if isinstance(detected, MembershipsList) else MembershipsList(detected)
        self._computeNodes()

    def get_nodes_count(self):
        return self.__nodesCount


    def get_original(self) -> MembershipsList:
        return self.__original

    def get_detected(self) -> MembershipsList:
        return self.__detected
    
    def __call__(self):
        return self.compare()
    
    def evaluate(self):
        aggregated = self._aggregate(self.get_original(), self.get_detected())
        selfAggregated = self.selfJaccard(aggregated)
        selfOriginal = self.selfJaccard(self.get_original())
        return self._frobenius(selfAggregated, selfOriginal)
    
    def selfJaccard(self, memberhips : MembershipsList) -> np.matrix:
        return self.jaccard(memberhips, memberhips)
    
    def jaccard(self, original : MembershipsList, detected : MembershipsList) -> np.matrix:
        return self._compare(original, detected, lambda a, b: self._setJaccard(a, b))
    
    def selfFraction(self, memberhips : MembershipsList) -> np.matrix:
        return self.jaccard(memberhips, memberhips)
    
    def fraction(self, original : MembershipsList, detected : MembershipsList) -> np.matrix:
        return self._compare(original, detected, lambda a, b: self._setFraction(a, b))
    
    def _aggregate(self, original : MembershipsList, detected : MembershipsList):
        matches = [self._bestMatch(m, original) for m in detected.getMemberships()]
        aggregated = self._joinByMatches(matches, detected, original.getCommunityCount())
        return MembershipsList(aggregated)
        
    def _bestMatch(self, members : list, original : MembershipsList):
        memberSet = set(members)
        maximum = 0
        maximumIndex = None
        for ci, m in enumerate(original.getMemberships()):
            value = self._setJaccard(memberSet, m)
            if value > maximum:
                maximum = value
                maximumIndex = ci
        return maximumIndex
    
    def _joinByMatches(self, matches : list, detected : MembershipsList, outComsCount : int):
        transposed = self._transposeMatches(matches, outComsCount)
        # spoji vrcholy v komunitach ze seznamu coms v transpozed
        # udela z nich mnozinu (odstrani se duplicity) a pak zase seznam 
        aggregated = [list(set([m for i in coms for m in detected.getCommunityMembers(i)])) for coms in transposed]
        return aggregated
    
    def _transposeMatches(self, matches : list, outComsCount : int) -> list:
        transposed = [[] for c in range(outComsCount)]
        for c, m in enumerate(matches):
            if m: transposed[m].append(c)
        return transposed
        
    def _compare(self, original : MembershipsList, detected : MembershipsList, metricsFcn : callable) -> np.matrix:
        matrix = np.zeros((original.getCommunityCount(), detected.getCommunityCount()))
        for dci in detected.getCommunities():
            detectedMembersSet = set(detected.getCommunityMembers(dci))
            for oci in original.getCommunities():
                matrix[dci, oci] = metricsFcn(detectedMembersSet, original.getCommunityMembers(oci))
        return matrix
    
    def _setJaccard(self, A, B):
        As = set(A)
        Bs = set(B)
        return float(len(As & Bs)) / len(As | Bs)
    
    def _setFraction(self, A, B):
        As = set(A)
        Bs = set(B)
        return float(len(As & Bs)) / self.get_nodes_count()
        
    def _frobenius(self, A, B):
        X = A - B 
        return np.sqrt(np.sum([x * x for x in X.flat]))
    
    def _computeNodes(self):
        nodes = set()    
        coms = self.get_original().getCommunities() + self.get_detected().getCommunities()
        for c in coms: nodes |= set(c)
        self.__nodesCount = len(nodes)

    original = property(get_original, None, None, "original community membership list")
    detected = property(get_detected, None, None, "detected detected membership list")
    nodesCount = property(get_nodes_count, None, None, "count of nodes")
