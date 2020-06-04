#!/usr/bin/env python3
import argparse
from classes.ProteomeDownloader import ProteomeDownloader

parser = argparse.ArgumentParser(description='Download proteomes from UniProt, according to the species list in tsv format.')
parser.add_argument('species_list', help='Species list in tsv format')
parser.add_argument('-n', '--cores', default=1, type=int, help='Number of CPU cores to be used for downloading proteome files.')
parser.add_argument('-o', '--outdir', default='proteome', help='Output directory')
parser.add_argument('-d', '--debug', action='store_true', help='For debug: do not download the genomes')
args = parser.parse_args()

downloader = ProteomeDownloader(args.outdir, args.species_list, args.cores)
downloader.download(args.debug)
