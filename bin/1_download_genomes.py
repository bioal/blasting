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

found = find_gcf(args.organism_list, summary_file)
with open(f'{args.outdir}/genomes_found.tsv', 'w') as fp:
    for no in sorted(found.keys(), key=int):
        print(no, found[no], sep='\t', file=fp)

def parse_url(url):
    # return server, path, filename
    url = url.replace('ftp://', '').replace('https://', '')
    dir_begin = url.find('/')
    dir_end = url.rfind('/')
    return url[0:dir_begin], url[dir_begin:], url[dir_end + 1:]

fp_out = open(f'{args.outdir}/genomes_downloaded.tsv', 'w')
for no in sorted(found.keys(), key=int):
    fields = found[no].split('\t')
    url = fields[19]
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
fp_out.close()
