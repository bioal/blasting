#!/usr/bin/env python3

import sys
from classes.DatabaseManager import DatabaseManager
from classes.OptionParser import OptionParser

parser = OptionParser(sys.argv)

database_folder = parser.get_option('o')
list_file = parser.get_option('l')
command = parser.get_option('p')
if command == None:
    command = 'makeblastdb'

if database_folder == None or list_file == None:
    print('Usage: make_database.py -o [output_folder] -l [list_file] -p [makeblastdb command (optional)]')
    print(' e.g., make_database.py -o /opt/orthology/data/genome/database -l gene_files.txt -p /user/local/bin/makeblastdb')
else:
    manager = DatabaseManager(database_folder, list_file, command)
    manager.make_database()

