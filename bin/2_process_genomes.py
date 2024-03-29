#!/usr/bin/env python3
import argparse
from classes.DataManager import DataManager

parser = argparse.ArgumentParser(description='Preprocess genome data for BLAST search.')
parser.add_argument('genome_list', help='List of downloaded genomes in tsv format')
parser.add_argument('-p', '--program', default='makeblastdb', help='Path to makeblsastdb command (default: makeblastdb)')
parser.add_argument('-o', '--outdir', default='data', help='Output directory')
args = parser.parse_args()

manager = DataManager(args.genome_list, args.program, f'{args.outdir}/genes', f'{args.outdir}/blastdb')
manager.preprocess()
