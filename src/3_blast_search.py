#!/usr/bin/env python3
import argparse
# import sys
from classes.BlastManager import BlastManager
# from classes.OptionParser import OptionParser

# parser = OptionParser(sys.argv)

# result_folder = parser.get_option('o')
# list_file = parser.get_option('l')
# num = parser.get_option('n')
# command = parser.get_option('p')
# if command == None:
#     command = 'blastp'

# if result_folder == None or list_file == None:
#     print('Usage: blast_search.py -o [output_folder] -l [list_file] -n [number of threads]')
#     print(' e.g., blast_search.py -o /opt/orthology/data/genome/blast -l databases.txt -n 4 -p /usr/local/bin/blastp')
# else:
#     manager = BlastManager(result_folder, list_file, num, command)
#     manager.search()

parser = argparse.ArgumentParser(description='BLAST search for the specified genomes.')
parser.add_argument('db_list', help='List of dbs in tsv format')
parser.add_argument('-n', '--threads', required=True, type=int, help='Number of threads to be used for BLAST')
parser.add_argument('-p', '--program', default='blastp', help='Path to blastp command (default: blastp)')
parser.add_argument('-o', '--outdir', default='blast', help='Output directory')
args = parser.parse_args()

manager = BlastManager(args.outdir, args.db_list, args.threads, args.program)
manager.search()
