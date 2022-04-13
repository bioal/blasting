#!/usr/bin/env python3
import argparse
from classes.BlastManager import BlastManager

parser = argparse.ArgumentParser(description='BLAST search for pairs of the specified organisms.')
parser.add_argument('genomes_downloaded', help='List of genomes downloaded')
parser.add_argument('pairs_file', help='Pairs of organisms to be compared')
parser.add_argument('-n', '--cores', required=True, type=int, help='Number of CPU cores to be used for BLAST')
parser.add_argument('-p', '--program', default='blastp', help='Path to blastp command (default: blastp)')
parser.add_argument('--dbdir', default='data/blastdb', help='blastdb directory')
parser.add_argument('-o', '--outdir', default='blast.out', help='Output directory')
args = parser.parse_args()

manager = BlastManager(args.program, args.cores, args.genomes_downloaded, args.dbdir, args.outdir)
manager.exec_pairs(args.pairs_file)
