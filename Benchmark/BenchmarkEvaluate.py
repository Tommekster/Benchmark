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
    return [eval(line) for line in open(file)]

def groupBy(records, *nargs):
    key = nargs[0]
    groups = {}
    output = []
    for r in records:
        group = str(r[key])
        if not group in groups:
            output.append({key:r[key], 'values': []})
            groups[group] = output[-1]['values']
        copy = dict(r)
        del copy[key]
        groups[group].append(copy)
    if len(nargs) > 1:
        keys = nargs[1:]
        for g in output:
            g['values'] = groupBy(g['values'], *keys)
    return output

if __name__ == '__main__':
    BenchmarkEvaluate()