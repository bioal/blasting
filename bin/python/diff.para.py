#!/usr/bin/env python3
import argparse
import os
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description='diff in parallel.')
parser.add_argument('files', nargs='+', help='files')
parser.add_argument('--target', required=True, help='target directory')
args = parser.parse_args()

def diff(file):
    target_file = os.path.join(args.target, file)
    subprocess.run(f'diff -q <(sort {file}) <(sort {target_file})', shell=True, executable='/usr/bin/bash')

with ThreadPoolExecutor(max_workers=48) as executor:
    executor.map(diff, args.files)
