#!/usr/bin/env python3
import argparse
from classes.BlastManager import BlastManager

parser = argparse.ArgumentParser(description='All aginst all BLAST for the specified organisms.')
parser.add_argument('organism_list', help='List of organisms in tsv format')
parser.add_argument('-n', '--cores', required=True, type=int, help='Number of CPU cores to be used for BLAST')
parser.add_argument('-p', '--program', default='blastp', help='Path to blastp command (default: blastp)')
parser.add_argument('-o', '--outdir', default='blast.out', help='Output directory')
args = parser.parse_args()

manager = BlastManager(args.program, args.cores, args.organism_list, 'data/blastdb', args.outdir)
manager.all_vs_all()
