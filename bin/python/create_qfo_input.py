#!/usr/bin/env python3
import sys
import csv

def extractUniProtAccessions(txt):
  return [elem.split('|')[1] for elem in txt.split(',')]

for i in range(1, len(sys.argv)):
  with open(sys.argv[i], encoding='utf-8', newline='') as f:
    csv_rows = csv.reader(f, delimiter='\t')
    next(csv_rows) # skip first line
    for cols in csv_rows:
      lhs_list = extractUniProtAccessions(cols[1])
      rhs_list = extractUniProtAccessions(cols[2])
      for lhs in lhs_list:
        for rhs in rhs_list:
          print(f"{lhs}\t{rhs}")
