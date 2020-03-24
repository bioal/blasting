#! /usr/local/bin/python

import sys
from classes.BlastManager import BlastManager
from classes.OptionParser import OptionParser

parser = OptionParser(sys.argv)

result_folder = parser.get_option('o')
list_file = parser.get_option('l')
num = parser.get_option('n')

if result_folder == None or list_file == None:
    print('Usage: blast_search.py -o [output_folder] -l [list_file] -n [number of threads]')
    print('    e.g., blast_search.py -o /opt/orthology/data/genome/blast -l databases.txt -n 4')
else:
    manager = BlastManager(result_folder, list_file, num)
    manager.search()

