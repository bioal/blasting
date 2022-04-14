#!/usr/bin/env python3
import os
import argparse
import subprocess
from threading import Thread, Semaphore
from functions import utils

parser = argparse.ArgumentParser(description='Summarize BLAST search resutls.')
parser.add_argument('organism_list', help='List of organisms in tsv format')
parser.add_argument('gene_refseq', help='List of organisms in tsv format')
parser.add_argument('-i', '--input', default='blast', help='BLAST results directory')
parser.add_argument('-o', '--outdir', default='bbh', help='Output directory')
parser.add_argument('-n', '--cores', required=True, type=int, help='Number of CPU cores to be used')
args = parser.parse_args()

semaphore = Semaphore(args.cores)

def extract_bbh(id1, id2):
    with semaphore:
        subprocess.run(f'./bin/perl/extract_bbh_gene.pl -i {args.input} {id1} {id2} {args.gene_refseq} > {args.outdir}/{id1}-{id2}.bbh_gene 2> {args.outdir}/{id1}-{id2}.bbh_gene.err', shell=True)

list = []
fp = open(args.organism_list)
for line in fp:
    fields = line.rstrip().split('\t')
    if utils.isint(fields[0]):
        list.append(fields[0])
fp.close

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

for i in range(0, len(list)):
    for j in range(i+1, len(list)):
        thread1 = Thread(target=extract_bbh, args=(list[i], list[j]))
        thread1.start()
        print('Queued ', list[i], list[j], flush=True)
