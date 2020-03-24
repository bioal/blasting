#! /usr/local/bin/python

import sys
from classes.DatabaseManager import DatabaseManager
from classes.OptionParser import OptionParser

parser = OptionParser(sys.argv)

database_folder = parser.get_option('o')
list_file = parser.get_option('l')

if database_folder == None or list_file == None:
    print('Usage: make_database.py -o [output_folder] -l [list_file]')
    print('    e.g., blast_search.py -o /opt/orthology/data/genome/database -l gene_files.txt')
else:
    manager = DatabaseManager(database_folder, list_file)
    manager.make_database()

