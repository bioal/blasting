#!/usr/bin/env python3
import argparse
from classes.GenomeDownloader2 import GenomeDownloader2

parser = argparse.ArgumentParser(description='Download genomes from NCBI, according to the species list in tsv format.')
parser.add_argument('species_list', help='Species list in tsv format')
parser.add_argument('-o', '--outdir', default='genome', help='Output directory')
parser.add_argument('-d', '--debug', action='store_true', help='For debug: do not download the genomes')
args = parser.parse_args()

downloader = GenomeDownloader2(args.outdir, args.species_list)
downloader.download(args.debug)
