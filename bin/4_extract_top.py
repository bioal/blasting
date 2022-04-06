#!/usr/bin/env python3
import argparse
import subprocess
from threading import Thread, Semaphore

parser = argparse.ArgumentParser(description='Extract BLAST results in parallel')
parser.add_argument('file', nargs='*', help='Input files')
parser.add_argument('-n', '--cores', required=True, type=int, help='Number of CPU cores to be used')
args = parser.parse_args()

semaphore = Semaphore(args.cores)

def conversion(f):
    with semaphore:
        subprocess.run(f'cat {f} | ../bin/perl/extract_top.pl > {f}.top 2> {f}.top.err', shell=True)

for f in args.file:
    t = Thread(target=conversion, args=(f,))
    t.start()
    print('Queued ' + f, flush=True)
