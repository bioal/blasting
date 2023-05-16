#!/usr/bin/env python3
import argparse
import os
from multiprocessing.pool import Pool
from multiprocessing import Manager

blast_out_dir = "/home/chiba/share/orth/blasting.homologene.2022-04/blast.out"
ncbi_gene_dir = "/home/chiba/share/ncbi/gene"
max_buffer_size = 1e8 # 100M lines ~ 10GB

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--symbol_list')
parser.add_argument('-o', '--out_dir', default='out')
parser.add_argument('-n', '--num_threads', type=int, default=48)
args = parser.parse_args()

os.makedirs(args.out_dir, exist_ok=True)

manager = Manager()
lock = manager.Lock()

input_symbols = set()
if args.symbol_list:
    with open(args.symbol_list, 'r') as f:
        for symbol in f.read().strip().split('\n'):
            input_symbols.add(symbol)

# Map from RefSeq protein ID to symbols
refseq_to_symbols = {}
with open(f"{ncbi_gene_dir}/gene2refseq_tax9606", 'r') as f:
    for line in f:
        tokens = line.strip().split("\t")
        protein = tokens[5]
        symbol = tokens[15]
        if protein != '-':
            if args.symbol_list and not symbol in input_symbols:
                continue
            refseq_to_symbols[protein] = symbol

def main():
    with Pool(processes=args.num_threads) as pool:
        for src_num in range(1, 22):
            pool.apply_async(process_a_file, args=(src_num, 1))
        for dst_num in range(2, 22):
            pool.apply_async(process_a_file, args=(1, dst_num))
        pool.close()
        pool.join()

def process_a_file(src_num, dst_num):
    buffer = {}
    count = 0
    def flush_buffer():
        with lock:
            for (symbol, lines) in buffer.items():
                with open(f"{args.out_dir}/{symbol}.out", "a") as dst:
                    dst.write("".join(lines))     
    with open(f"{blast_out_dir}/{src_num}-{dst_num}.out", "r") as f:
        for line in f:
            row = line.strip().split("\t")
            query = row[0].strip()
            target = row[1].strip()
            symbols = set()
            if query in refseq_to_symbols:
                symbols.add(refseq_to_symbols[query])
            if target in refseq_to_symbols:
                symbols.add(refseq_to_symbols[target])
            for symbol in symbols:
                if symbol not in buffer.keys():
                    buffer[symbol] = []
                buffer[symbol].append(f"{src_num}-{dst_num}.out:{line}")
                count += 1
                if count >= max_buffer_size:
                    flush_buffer()
                    buffer = {}
                    count = 0
    flush_buffer()

if __name__ == '__main__':
    main()
