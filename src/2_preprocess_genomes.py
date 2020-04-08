#!/usr/bin/env python3
import argparse
from classes.DatabaseManager import DatabaseManager

parser = argparse.ArgumentParser(description='Preprocess genome data for BLAST search.')
parser.add_argument('genome_file_list', help='List of downloaded genome files in tsv format')
parser.add_argument('-o', '--outdir', default='.', help='Output directory')
parser.add_argument('--makedb', action='store_true', help='Execute makeblastdb')
parser.add_argument('-p', '--program', default='makeblastdb', help='Path to makeblastdb')
args = parser.parse_args()

manager = DatabaseManager(args.outdir, args.genome_file_list, args.makedb, args.program)
manager.preprocess()
