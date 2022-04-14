#!/usr/bin/env python3
import os
import re
import argparse
import subprocess
from classes.FtpCli import FtpCli
from functions.find_gcf_file import find_gcf

parser = argparse.ArgumentParser(description='Download genomes from NCBI, according to the organism list in tsv format.')
parser.add_argument('organism_list', help='Organism list in tsv format')
parser.add_argument('-o', '--outdir', default='data', help='Output directory')
args = parser.parse_args()

out_dir = f'{args.outdir}/genomes'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

ftp = FtpCli('ftp.ncbi.nlm.nih.gov')
ftp_dir = '/genomes/ASSEMBLY_REPORTS/'
file_name = 'assembly_summary_refseq.txt'
summary_file = args.outdir + '/' + file_name
ftp.sync(ftp_dir + file_name, summary_file)
ftp.close()

genomes_found = f'{args.outdir}/genomes_found.tsv'
found = find_gcf(args.organism_list, summary_file)
with open(genomes_found, 'w') as fp:
    for no in sorted(found.keys(), key=int):
        print(no, found[no], sep='\t', file=fp)

def parse_url(url):
    url = url.replace('ftp://', '').replace('https://', '')
    i_dir = url.find('/')
    i_base = url.rfind('/')
    server = url[0:i_dir]
    path = url[i_dir:]
    name = url[i_base + 1:]
    return server, path, name

fp = open(genomes_found, 'r', encoding='UTF-8')
fp_out = open(f'{args.outdir}/genomes_downloaded.tsv', 'w')
for line in fp:
    line = line.rstrip()
    fields = line.split('\t')
    no = fields[0]
    url = fields[20]
    url_server, url_path, url_name = parse_url(url)
    if url.endswith('gz'):
        gz_file_path = url_path
        gz_file_name = url_name
    else:
        gz_file_path = f'{url_path}/{url_name}_protein.faa.gz'
        gz_file_name = f'{url_name}_protein.faa.gz'
    genome_file_name = re.sub(r'.gz', '', gz_file_name)
    ftp = FtpCli(url_server)
    ftp.sync(gz_file_path, f'{out_dir}/{gz_file_name}')
    ftp.close()
    print(f'{no}\t{out_dir}/{genome_file_name}', file=fp_out, flush=True)
fp.close()
fp_out.close()
