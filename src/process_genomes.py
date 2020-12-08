#!/usr/bin/env python3
import argparse
from classes.FASTA import FASTA

parser = argparse.ArgumentParser(description='Preprocess genome data')
parser.add_argument('genome_id', help='Genome ID')
args = parser.parse_args()

gcf_files = {}
genome_file_list = 'genome_list.tsv'
fp = open(genome_file_list, 'r')
for line in fp:
    fields = line.strip().split('\t')
    id = fields[0]
    gcf_file = fields[1]
    gcf_files[id] = gcf_file

fasta_file = gcf_files[args.genome_id]

fasta = FASTA(fasta_file)
fasta.preprocess()
