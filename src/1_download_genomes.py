#!/usr/bin/env python3
import sys
import argparse
from classes.GenomeDownloader import GenomeDownloader

parser = argparse.ArgumentParser(description='Download genomes from NCBI, according to the species list in tsv format.')
parser.add_argument('species_list', help='Species list in tsv format')
parser.add_argument('-o', '--outdir', default='genomes', help='Output directory')
parser.add_argument('-d', '--debug', action='store_true', help='For debug: do not download the genomes')
args = parser.parse_args()

downloader = GenomeDownloader(args.outdir, args.species_list)
downloader.download(args.debug)
