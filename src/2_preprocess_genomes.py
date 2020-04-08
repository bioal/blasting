#!/usr/bin/env python3
import argparse
from classes.DatabaseManager import DatabaseManager

parser = argparse.ArgumentParser(description='Preprocess genome data for BLAST search.')
parser.add_argument('genome_file_list', help='List of downloaded genome files in tsv format')
parser.add_argument('-p', '--program', default='makeblastdb', help='Path to makeblsastdb command (default: makeblastdb)')
args = parser.parse_args()

manager = DatabaseManager(args.genome_file_list, args.program)
manager.preprocess()
