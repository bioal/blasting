#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='Summarize BLAST search resutls.')
parser.add_argument('matrix', help='matrix')
args = parser.parse_args()

fp = open(args.matrix, 'r')
line = fp.readline()
line = line.rstrip('\n')
countDict = {}
lineDict = {}
print(line)
for line in fp:
    line = line.rstrip('\n')
    fields = line.split('\t')
    id = fields[0]
    values = fields[1:]
    count = 0
    for v in values:
        if v == '1':
            count += 1
    # print(values)
    # print(count, '\t'.join(values), sep='\t')
    lineDict[id] = line
    countDict[id] = count
    

fp.close()

sortedDict = sorted(countDict.items(), key=lambda x:x[1], reverse=True)
for id, val in sortedDict:
    print(lineDict[id])
