#!/usr/bin/env python3
import argparse
import subprocess

parser = argparse.ArgumentParser(description='BLAST search for the specified genomes.')
parser.add_argument('query_id', help='Query genome ID')
parser.add_argument('db_id', help='DB genome ID')
parser.add_argument('-o', '--outfile', help='Output file')
parser.add_argument('-e', '--errfile', help='Error file')
parser.add_argument('-f', '--format', default='6', help='Output format')
parser.add_argument('-m', '--max', default='1', help='max_target_seq')
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
    '-outfmt', args.format,
    '-max_target_seqs', args.max
]

if args.outfile:
    command += ['-out', args.outfile]

subprocess.run(command)

if args.errfile:
    ret = subprocess.run(command, stderr=subprocess.PIPE)
    fp = open(args.errfile, 'w')
    fp.write(ret.stderr.decode())
    fp.close()
