#!/usr/bin/env python3
import argparse
import os
import glob
import subprocess
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description='Summarize scores of each gene in parallel.')
parser.add_argument('-o', '--outdir', default='summarized_score', help='Output directory')
args = parser.parse_args()

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

dbm_path = '/home/chiba/github/bioal/blasting/examples/seq_descr.dbm'
top_score_path = '/mnt/share/chiba/orth/blasting.homologene.2022-04/top_score_to_human'
file_paths = glob.glob('*.out')

def run_command(file_path):
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    out_file_path = os.path.join(args.outdir, file_name)
    command = f'/home/chiba/github/bioal/blasting/bin/perl/summarize_scores_with_descr.pl -v -t {top_score_path} -d {dbm_path} {file_path} > {out_file_path}.scores.txt 2> {out_file_path}.scores.err'
    subprocess.run(['bash', '-c', command])

with ThreadPoolExecutor(max_workers=96) as executor:
    executor.map(run_command, file_paths)
