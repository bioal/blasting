#!/usr/bin/env python3
import argparse
from classes.RDFManager import RDFManager

parser = argparse.ArgumentParser(description='Make RDF for genome list')
parser.add_argument('genome_summary', help='Genome summary file')
# parser.add_argument('-p', '--program', default='makeblastdb', help='Path to makeblsastdb command (default: makeblastdb)')
args = parser.parse_args()

manager = RDFManager(args.genome_summary)
manager.create_rdf()
