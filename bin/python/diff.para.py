#!/usr/bin/env python3
import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description='diff in parallel.')
parser.add_argument('files', nargs='+', help='files')
parser.add_argument('--target', required=True, help='target directory')
args = parser.parse_args()

def diff(file):
    return subprocess.run(f'diff <(sort {file}) <(sort {args.target}/{file})', shell=True, executable='/usr/bin/bash', stdout=subprocess.PIPE)

future_list = []
with ThreadPoolExecutor(os.cpu_count() // 2) as executor:
    for file in args.files:
        future = executor.submit(diff, file)
        future_list.append(future)

for i in range(len(args.files)):
    result = future_list[i].result()
    if result.returncode:
        print(f'== {args.files[i]} ==')
        print(result.stdout.decode())
