#!/usr/bin/env python3
import os
import re
import argparse
import subprocess
from classes.FtpCli import FtpCli

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
subprocess.run(f'./bin/perl/find_gcf_file.pl {args.organism_list} {summary_file} | sort -n > {genomes_found}', shell=True)

fp = open(genomes_found, 'r', encoding='UTF-8')
fp_out = open(f'{args.outdir}/genomes_downloaded.tsv', 'w')
for line in fp:
    line = line.rstrip()
    fields = line.split('\t')
    no = fields[0]
    url = fields[20]
    server = url.replace('ftp://', '')
    server = url.replace('https://', '')
    index = server.find('/')
    path = server[index:]
    server = server[0:index]
    index = path.rfind('/')
    name = path[index + 1:]
    if name.endswith('gz'):
        gz_file_name = name
        gz_file_path = path
    else:
        gz_file_name = name + '_protein.faa.gz'
        gz_file_path = f'{path}/{gz_file_name}'
    ftp = FtpCli(server)
    ftp.sync(gz_file_path, f'{out_dir}/{gz_file_name}')
    ftp.close()
    genome_file_name = re.sub(r'.gz', '', gz_file_name)
    print(f'{no}\t{out_dir}/{genome_file_name}', file=fp_out, flush=True)
fp.close()
fp_out.close()
