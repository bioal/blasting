#!/usr/bin/env python3
import os
import argparse
import subprocess
from classes.FtpCli import FtpCli
from classes.GenomeDownloader import GenomeDownloader

parser = argparse.ArgumentParser(description='Download genomes from NCBI, according to the species list in tsv format.')
parser.add_argument('species_list', help='Species list in tsv format')
parser.add_argument('-n', '--cores', default=1, type=int, help='Number of CPU cores to be used for downloading genome files.')
parser.add_argument('-o', '--outdir', default='data', help='Output directory')
parser.add_argument('-d', '--debug', action='store_true', help='For debug: do not download the genomes')
args = parser.parse_args()

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

ftp = FtpCli('ftp.ncbi.nlm.nih.gov')
ftp_dir = '/genomes/ASSEMBLY_REPORTS/'
file_name = 'assembly_summary_refseq.txt'
summary_file = args.outdir + '/' + file_name
ftp.sync(ftp_dir + file_name, summary_file)
ftp.close()

genomes_found = f'{args.outdir}/genomes_found.tsv'
subprocess.run(f'./bin/perl/find_gcf_file.pl {args.species_list} {summary_file} | sort -n > {genomes_found}', shell=True)

downloader = GenomeDownloader(args.outdir + '/genome', args.cores)
downloader.sync(genomes_found, args.outdir + '/genome.tsv', args.outdir + '/genome.err', args.debug)
