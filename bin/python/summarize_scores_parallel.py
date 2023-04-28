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

def summarize(file_path):
    dbm_path = '/home/chiba/github/bioal/blasting/examples/seq_descr.dbm'
    top_score_to_human = '/mnt/share/chiba/orth/blasting.homologene.2022-04/top_score_to_human'
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    out_path = os.path.join(args.outdir, name)
    subprocess.run(f'/home/chiba/github/bioal/blasting/bin/perl/summarize_scores_with_descr.pl -v -t {top_score_to_human} -d {dbm_path} {file_path} > {out_path}.scores.txt 2> {out_path}.scores.err', shell=True)

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    files = glob.glob('*.out')
    executor.map(summarize, files)
