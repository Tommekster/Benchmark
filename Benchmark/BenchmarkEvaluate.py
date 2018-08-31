'''
Created on 31. 8. 2018

@author: Tomáš
'''
import json

BENCHMARK_FILE = 'benchmark.txt'

def BenchmarkEvaluate(inputFile, outputFile):
    print(' '.join([inputFile, outputFile]))
    records = loadRecords(inputFile)
    runs = groupBy(records, 'graph','params')
    means = computeMeans(runs, 'evaluations')
    #print(json.dumps(means, indent=4))
    with open(outputFile,'w') as f: f.write(json.dumps(means, indent=4))
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

def computeMeans(groups, field):
    output = []
    for group in groups:
        means = {k: 0 for k in group['values'][0][field]}
        squared = {k: 0 for k in means}
        for value in group['values']:
            for k in means: 
                means[k] += value[field][k]
                squared[k] += value[field][k] ** 2
        for k in means: 
            means[k] /= len(group['values'])
            squared[k] /= len(group['values'])
        stdev = {k: abs(squared[k] - means[k] ** 2) ** (1/2) for k in means}
        dev = {k: 1.96*stdev[k] for k in stdev}
        copy = dict(group)
        del copy['values']
        copy['mean'] = means
        copy['stdev'] = stdev
        copy['dev'] = dev
        output.append(copy)
    return output

if __name__ == '__main__':
    BenchmarkEvaluate('output/benchmark2.txt', 'output/unipartitni.txt')
    BenchmarkEvaluate('output/benchmark4.txt', 'output/comNums.txt')