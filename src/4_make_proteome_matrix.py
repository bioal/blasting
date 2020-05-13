#!/usr/bin/env python3
import argparse
from classes.ProteomeMatrixManager import MatrixManager

parser = argparse.ArgumentParser(description='Summarize BLAST search resutls.')
parser.add_argument('proteome_list', help='List of proteome in tsv format')
parser.add_argument('-i', '--input', required=True, help='BLAST results directory')
parser.add_argument('-o', '--outdir', default='matrix', help='Output directory')
args = parser.parse_args()

manager = MatrixManager(args.input, args.outdir, args.proteome_list)
manager.make_matrix()
