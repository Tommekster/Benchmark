'''
Created on 31. 8. 2018

@author: Tomáš
'''
import json

BENCHMARK_FILE = 'benchmark.txt'

def BenchmarkEvaluate():
    records = loadRecords(BENCHMARK_FILE)
    runs = groupBy(records, 'graph','params')
    print(json.dumps(runs, indent=4))
    #means = computeMean(runs, 'evaluations')
    #printResults(means)
    
def loadRecords(file):
    return (eval(line) for line in open(file))

def groupBy(records, *nargs, keyAsTuple=True):
    if keyAsTuple:
        keys = nargs[:]
    else: 
        keys = nargs[0]
    groups = {}
    output = []
    for r in records:
        group = str([r[key] for key in keys])
        if not group in groups:
            output.append({key:r[key] for key in keys})
            output[-1]['values'] = []
            groups[group] = output[-1]['values']
        copy = dict(r)
        for key in keys: del copy[key]
        groups[group].append(copy)
    if not keyAsTuple and len(nargs) > 1:
        _keys = nargs[1:]
        for g in output:
            g['values'] = groupBy(g['values'], *_keys)
    return output

def computeMeans(runs, field):
    #return (dict(graph=graph, params= ))
    pass

if __name__ == '__main__':
    BenchmarkEvaluate()