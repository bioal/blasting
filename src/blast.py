#!/usr/bin/env python3
import argparse
import subprocess

parser = argparse.ArgumentParser(description='BLAST search for the specified genomes.')
parser.add_argument('query_id', help='Query genome ID')
parser.add_argument('db_id', help='DB genome ID')
parser.add_argument('-l', '--list', default='proteome_list.tsv', help='Input file list')
parser.add_argument('-o', '--outfile', default='blast.out', help='Output file')
parser.add_argument('-e', '--errfile', default='blast.err', help='Error file')
parser.add_argument('-E', '--evalue', default='0.001', help='E-value threshold')
parser.add_argument('-f', '--format', default='7', help='Output format')
# parser.add_argument('-m', '--max', default='1', help='max_target_seq')
args = parser.parse_args()

fasta_files = {}
fp = open(args.list, 'r')
for line in fp:
    fields = line.strip().split('\t')
    id = fields[0]
    fasta_file = fields[1]
    fasta_files[id] = fasta_file

query_file = fasta_files[args.query_id]
# db_file = fasta_files[args.db_id]
db_file = 'db/' + args.db_id
    
command = ['blastp', '-query', query_file, '-db', db_file, '-outfmt', args.format
    # '-max_target_seqs', args.max
]

if args.outfile:
    command += ['-out', args.outfile]

subprocess.run(command)

if args.errfile:
    ret = subprocess.run(command, stderr=subprocess.PIPE)
    fp = open(args.errfile, 'w')
    fp.write(ret.stderr.decode())
    fp.close()
