#!/usr/bin/env python3
import argparse
from classes.DataManager import DataManager

parser = argparse.ArgumentParser(description='Preprocess genome data for BLAST search.')
parser.add_argument('genomes_list', help='List of downloaded genomes in tsv format')
parser.add_argument('-p', '--program', default='makeblastdb', help='Path to makeblsastdb command (default: makeblastdb)')
args = parser.parse_args()

manager = DataManager(args.genomes_list, args.program)
manager.preprocess()
