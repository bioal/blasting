#!/usr/bin/env python3
import argparse
from classes.ResultManager import ResultManager

parser = argparse.ArgumentParser(description='Summarize BLAST search resutls.')
parser.add_argument('organism_list', default='proteome_list.tsv', help='List of organisms in tsv format')
parser.add_argument('-i', '--input', default='blast', help='BLAST results directory')
parser.add_argument('-o', '--outdir', default='matrix', help='Output directory')
args = parser.parse_args()

manager = ResultManager(args.input, args.outdir, args.organism_list)
manager.calc_bbh()
