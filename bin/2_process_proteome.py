#!/usr/bin/env python3
import argparse
from classes.ProteomeManager import ProteomeManager

parser = argparse.ArgumentParser(description='Preprocess proteome data for BLAST search.')
parser.add_argument('proteome_list', help='List of downloaded proteomes in tsv format')
parser.add_argument('-p', '--program', default='makeblastdb', help='Path to makeblsastdb command (default: makeblastdb)')
args = parser.parse_args()

manager = ProteomeManager(args.proteome_list, args.program)
manager.preprocess()
