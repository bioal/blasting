#!/usr/bin/env python3
import argparse
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description='diff in parallel.')
parser.add_argument('files', nargs='+', help='files')
parser.add_argument('-s', '--sort', action='store_true')
parser.add_argument('-q', '--brief', action='store_true')
parser.add_argument('-t', '--to', required=True, help='target directory')
args = parser.parse_args()

command = "diff"
if args.brief:
    command += " -q"

def diff(file_path):
    file_name = os.path.basename(file_path)
    if args.sort:
        return subprocess.run(f'{command} <(sort {file_path}) <(sort {args.to}/{file_name})', shell=True, executable='/usr/bin/bash', stdout=subprocess.PIPE)
    else:
        return subprocess.run(f'{command} {file_path} {args.to}/{file_name}', shell=True, executable='/usr/bin/bash', stdout=subprocess.PIPE)

future_list = []
with ThreadPoolExecutor(os.cpu_count() // 2) as executor:
    for file in args.files:
        future_list.append(executor.submit(diff, file))

for i in range(len(args.files)):
    result = future_list[i].result()
    if result.returncode:
        file_name = os.path.basename(args.files[i])
        print(f'== {file_name} ==')
        print(result.stdout.decode())
