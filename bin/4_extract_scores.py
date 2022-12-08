#!/usr/bin/env python3
import os
import argparse
import subprocess
from threading import Thread, Semaphore

parser = argparse.ArgumentParser(description='Extract BLAST results in parallel')
parser.add_argument('gene', nargs='*', help='Genes')
# parser.add_argument('gene_list', help='Gene list')
parser.add_argument('-n', '--cores', required=True, type=int, help='Number of CPU cores to be used')
args = parser.parse_args()

semaphore = Semaphore(args.cores)

def conversion(gene):
    with semaphore:
        subprocess.run(f'grep -w {gene} *.out > gene/{gene}.out 2> gene/{gene}.err', shell=True)

if not os.path.exists('gene'):
    os.makedirs('gene')

# ret = subprocess.run(f'cat {args.gene_list} | cut 2', stdout=subprocess.PIPE, shell=True)
# genes = ret.stdout.decode().rstrip().split('\n')

for gene in args.gene:
    t = Thread(target=conversion, args=(gene,))
    t.start()
    print('Queued ' + gene, flush=True)
