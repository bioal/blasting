#!/usr/bin/env python3
import argparse
from classes.MatrixManager import MatrixManager

parser = argparse.ArgumentParser(description='Summarize BLAST search resutls.')
parser.add_argument('genome_list', help='List of genomes in tsv format')
parser.add_argument('-i', '--input', required=True, help='BLAST results directory')
parser.add_argument('-o', '--outdir', default='matrix', help='Output directory')
args = parser.parse_args()

manager = MatrixManager(args.outdir, args.genome_list, args.input)
manager.make_matrix()
