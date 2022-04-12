#!/usr/bin/env python3
import re
import argparse

parser = argparse.ArgumentParser(description='Find genomes of organism_list from assembly_reports')
parser.add_argument('organism_list', help='List of organisms in tsv format')
parser.add_argument('assembly_reports', help='Assembly reports file')
args = parser.parse_args()

org = {}
fp1 = open(args.organism_list, 'r')
for line in fp1:
    line = line.rstrip('\r\n')
    fields = line.split('\t')
    no = fields[0]
    taxid = fields[1]
    if re.match(r'^[1-9][0-9]*$', no):
        org[taxid] = no
fp1.close()

fp2 = open(args.assembly_reports, 'r', encoding='UTF-8')
for line in fp2:
    line = line.rstrip('\r\n')
    fields = line.split('\t')
    if line.startswith('#'):
        continue
    if len(fields) >= 7:
        category = fields[4]
        taxid = fields[5]
        species_taxid = fields[6]
        if category == "na":
            continue
        if taxid in org:
            print(org[taxid] + '\t' + line)
        elif species_taxid in org:
            print(org[species_taxid] + '\t' + line)
fp2.close()
