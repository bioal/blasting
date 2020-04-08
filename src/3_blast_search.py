#!/usr/bin/env python3
import argparse
from classes.BlastManager import BlastManager

parser = argparse.ArgumentParser(description='BLAST search for the specified genomes.')
parser.add_argument('db_list', help='List of dbs in tsv format')
parser.add_argument('-n', '--threads', required=True, type=int, help='Number of threads to be used for BLAST')
parser.add_argument('-p', '--program', default='blastp', help='Path to blastp command (default: blastp)')
parser.add_argument('-o', '--outdir', default='blast', help='Output directory')
args = parser.parse_args()

manager = BlastManager(args.outdir, args.db_list, args.threads, args.program)
manager.search()
