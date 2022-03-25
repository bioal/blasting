#!/usr/bin/env python3
import argparse
from classes.BBH import BBH

parser = argparse.ArgumentParser(description='Summarize BLAST search resutls.')
parser.add_argument('organism_list', help='List of organisms in tsv format')
parser.add_argument('--blastdir', default='blast', help='BLAST results directory')
parser.add_argument('-o', '--outdir', default='matrix', help='Output directory')
args = parser.parse_args()

manager = BBH(args.blastdir, args.outdir, args.organism_list)
manager.calc_bbh()
