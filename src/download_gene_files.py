#! /usr/local/bin/python

import sys
from classes.GeneDownloader import GeneDownloader
from classes.OptionParser import OptionParser

parser = OptionParser(sys.argv)

data_folder = parser.get_option('o')
list_file = parser.get_option('l')

if data_folder == None or list_file == None:
    print('Usage: download_gene_files.py -o [output_folder] -l [list_file]')
    print('    e.g., download_gene_files.py -o /opt/orthology/data/genome -l /opt/orthology/data/species_list.tsv')
else:
    downloader = GeneDownloader(data_folder, list_file)
    downloader.download()

