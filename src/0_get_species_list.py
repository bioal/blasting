#!/usr/bin/env python3
import argparse
import requests

parser = argparse.ArgumentParser(description='Get the target species list in tsv format.')
parser.add_argument('-o', '--outfile', default='species_list.tsv', help='Output file')
args = parser.parse_args()

response = requests.get('https://docs.google.com/spreadsheets/d/1-7FY-B_BpU72A045EeEuExea6FtMs8q-Urn9-R6-TWk/export?format=tsv')

fp = open(args.outfile, 'w')

fp.write(response.text)

fp.close()
