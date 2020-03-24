#! /usr/local/bin/python

import sys
from classes.MatrixManager import MatrixManager
from classes.OptionParser import OptionParser

parser = OptionParser(sys.argv)

matrix_folder = parser.get_option('o')
list_file = parser.get_option('l')
input_folder = parser.get_option('i')

if matrix_folder == None or list_file == None or input_folder == None:
    print('Usage: make_matrix.py -o [output_folder] -l [list_file] -i [input_folder]')
    print('    e.g., make_matrix.py -o /opt/orthology/data/genome/matrix -l databases.txt -i /opt/orthology/data/genome/blast')
else:
    manager = MatrixManager(matrix_folder, list_file, input_folder)
    manager.make_matrix()

