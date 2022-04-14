#!/usr/bin/env python3
import re

def find_gcf(organism_list, assembly_reports):
    org = {}
    fp1 = open(organism_list, 'r')
    for line in fp1:
        line = line.rstrip('\r\n')
        fields = line.split('\t')
        no = fields[0]
        taxid = fields[1]
        if re.match(r'^[1-9][0-9]*$', no):
            org[taxid] = no
    fp1.close()

    found = {}
    fp2 = open(assembly_reports, 'r', encoding='UTF-8')
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
            no = org.get(taxid) or org.get(species_taxid)
            if no is not None:
                found[no] = line
    fp2.close()
    
    return found

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Find genomes of organism_list from assembly_reports')
    parser.add_argument('organism_list', help='List of organisms in tsv format')
    parser.add_argument('assembly_reports', help='Assembly reports file')
    args = parser.parse_args()
    
    found = find_gcf(args.organism_list, args.assembly_reports)
    for no in sorted(found.keys(), key=int):
        print(no, found[no], sep='\t')
