'''
Created on 31. 8. 2018

@author: Tomáš
'''
import json
import matplotlib.pyplot as plt
import numpy as np

BENCHMARK_FILE = 'benchmark.txt'


def BenchmarkEvaluate(inputFile, outputFile):
    print(' '.join([inputFile, outputFile]))
    records = loadRecords(inputFile)
    runs = groupBy(records, 'graph', 'params')
    means = computeMeans(runs, 'evaluations')
    with open(outputFile, 'w') as f: f.write(json.dumps(means, indent=4))
    plotEvaluations(means, outputFile + '.png', values=False, a4paper=False)
    plotEvaluations(means, outputFile + '.pdf', labels=False)
    plotEvaluations(means, outputFile + '.T.pdf', labels=False, transpose=True,
                    mathshowArgs=dict(aspect=0.3))
    texTable(means, outputFile + '.tex')

    
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
        stdev = {k: abs(squared[k] - means[k] ** 2) ** (1 / 2) for k in means}
        dev = {k: 1.96 * stdev[k] for k in stdev}
        copy = dict(group)
        del copy['values']
        copy['mean'] = means
        copy['squared'] = squared
        copy['stdev'] = stdev
        copy['dev'] = dev
        output.append(copy)
    return output


def plotEvaluations(means, imageFile, headers=True, values=True, labels=True,
                    a4paper=True, transpose=False, fontsize=8, mathshowArgs=dict()):
    # _headers = [k for k in means[0]['mean']]
    _headers = ['louvain', 'olapSBMmax', 'olapSBM', 'bigClam', 'biSBM']
    data = np.array([[row['mean'][k] for k in _headers] for row in means])
    conf = np.array([[row['dev'][k] for k in _headers] for row in means])
    if transpose:
        data = data.transpose()
        conf = conf.transpose()
    params = [str(row['params']) for row in means]
    
    _, ax = plt.subplots()
    matshowkw = dict(cmap='seismic')
    matshowkw.update(mathshowArgs)
    ax.matshow(data, **matshowkw)
    
    if values:
        for (i, j), z in np.ndenumerate(data):
            ax.text(j, i, '{:0.3f}±{:0.3f}'.format(z, conf[i, j]), ha='center', va='center',
                    fontsize=fontsize,
                    bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))
    ax.set_xticks(np.arange(data.shape[1]), minor=False)
    ax.set_yticks(np.arange(data.shape[0]), minor=False)
    if transpose:
        if headers: ax.set_yticklabels(_headers)
        if labels: ax.set_xticklabels(params, rotation=90)
        else: ax.set_xticklabels([i + 1 for i in range(len(params))])
        ax.xaxis.set_ticks_position('bottom')
    else:
        if headers: ax.set_xticklabels(_headers, rotation=90)
        if labels: ax.set_yticklabels(params)
        else: ax.set_yticklabels([i + 1 for i in range(len(params))])
    if a4paper:
        dim = (11.69, 8.27) if transpose else (8.27, 11.69)
        plt.gcf().set_size_inches(dim)
        
    plt.savefig(imageFile)
    plt.close()


def texTable(means, texFile):
    # _headers = [k for k in means[0]['mean']]
    _headers = ['louvain', 'olapSBMmax', 'olapSBM', 'bigClam', 'biSBM']
    with open(texFile, 'w') as f:
        f.write(' & '.join(_headers) + '\\\\ \\hline \n')
        for row in means: f.write(' & '.join(['{:0.3f}$\\pm${:0.3f}'.format(row['mean'][k], row['dev'][k]) for k in _headers]) + '\\\\\n')
    

if __name__ == '__main__':
    BenchmarkEvaluate('output/benchmarkUnipartite.txt', 'output/unipartitni.txt')
    BenchmarkEvaluate('output/benchmarkBipartite.txt', 'output/bipartitni.txt')
    BenchmarkEvaluate('output/benchmarkComNumsUni.txt', 'output/comNumsUni.txt')
    BenchmarkEvaluate('output/benchmarkComNumsBi.txt', 'output/comNumsBi.txt')
    BenchmarkEvaluate('output/benchmarkBipartite2.txt', 'output/bipartitni2.txt')