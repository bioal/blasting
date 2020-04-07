#!/usr/bin/env python3

import sys
from classes.GenomeDownloader import GenomeDownloader
from classes.OptionParser import OptionParser

parser = OptionParser(sys.argv)

# list_file = parser.get_option('l')

data_folder = parser.get_option('o')
if data_folder == None:
    data_folder = 'genomes'

if data_folder == None or len(sys.argv) != 1:
    print('Usage: download_gene_files.py -o [output_folder] -l [list_file]')
    print(' e.g., download_gene_files.py -o /opt/orthology/data/genome -l /opt/orthology/data/species_list.tsv')
else:
    list = sys.argv[0]
    downloader = GenomeDownloader(data_folder, list_file)
    downloader.download()

