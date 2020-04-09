#!/usr/bin/env python3
import argparse
from classes.BlastManager import BlastManager

parser = argparse.ArgumentParser(description='BLAST search for the specified genomes.')
parser.add_argument('genome_list', help='List of genomes in tsv format')
parser.add_argument('-n', '--cores', required=True, type=int, help='Number of CPU cores to be used for BLAST')
parser.add_argument('-p', '--program', default='blastp', help='Path to blastp command (default: blastp)')
parser.add_argument('-o', '--outdir', default='blast', help='Output directory')
args = parser.parse_args()

manager = BlastManager(args.program, args.cores, args.genome_list, args.outdir)
manager.search()
