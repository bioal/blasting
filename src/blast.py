#!/usr/bin/env python3
import argparse
import subprocess

parser = argparse.ArgumentParser(description='BLAST search for the specified genomes.')
parser.add_argument('query_id', help='Query genome ID')
parser.add_argument('db_id', help='DB genome ID')
parser.add_argument('-f', '--format', default='6', help='Output format')
parser.add_argument('-o', '--outfile', help='Output file')
args = parser.parse_args()

gcf_files = {}
genome_file_list = 'genome_list.tsv'
fp = open(genome_file_list, 'r')
for line in fp:
    fields = line.strip().split('\t')
    id = fields[0]
    gcf_file = fields[1]
    gcf_files[id] = gcf_file

query_file = gcf_files[args.query_id]
db_file = 'db/' + args.db_id
    
command = [
    'blastp',
    '-query', query_file,
    '-db', db_file,
    '-max_target_seqs', '1',
    '-outfmt', args.format,
    '-out', args.outfile
]

subprocess.run(command)
