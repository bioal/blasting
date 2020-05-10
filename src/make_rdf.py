#!/usr/bin/env python3
import argparse
from classes.RDFManager import RDFManager

parser = argparse.ArgumentParser(description='Make RDF')
parser.add_argument('summary_file', help='Summary file')
parser.add_argument('-p', '--proteome', action='store_true', help='For proteome')
# parser.add_argument('-p', '--program', default='makeblastdb', help='Path to makeblsastdb command (default: makeblastdb)')
args = parser.parse_args()

manager = RDFManager(args.summary_file)
if args.proteome:
    manager.rdfize_proteome()
else:
    manager.rdfize_genome()
