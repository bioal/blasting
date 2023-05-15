#!/usr/bin/env python3
import argparse
import os
from multiprocessing.pool import Pool
from multiprocessing import Manager

blast_out_dir = "/home/chiba/share/orth/blasting.homologene.2022-04/blast.out"
ncbi_gene_dir = "/home/chiba/share/ncbi/gene"

parser = argparse.ArgumentParser()
parser.add_argument('query_symbol_list')
parser.add_argument('-o', '--out_dir', default='out')
parser.add_argument('-n', '--num_threads', type=int, default=48)
args = parser.parse_args()

os.makedirs(args.out_dir, exist_ok=True)

manager = Manager()
lock = manager.Lock()

# Read gene symbols
symbol_dict = {}
with open(args.query_symbol_list, 'r') as f:
    for symbol in f.read().strip().split('\n'):
        symbol_dict[symbol] = True

# Map from RefSeq protein ID to symbols
refseq_to_symbols = {}
with open(f"{ncbi_gene_dir}/gene2refseq_tax9606", 'r') as f:
    for line in f:
        tokens = line.strip().split("\t")
        protein = tokens[5]
        symbol = tokens[15]
        if protein != '-':
            if not symbol in symbol_dict:
                continue
            if protein not in refseq_to_symbols:
                refseq_to_symbols[protein] = []
            refseq_to_symbols[protein].append(symbol)

def main():
    with Pool(processes=args.num_threads) as pool:
        for src_num in range(1, 22):
            pool.apply_async(process_a_file, args=(src_num, 1))
        for dst_num in range(2, 22):
            pool.apply_async(process_a_file, args=(1, dst_num))
        pool.close()
        pool.join()

def process_a_file(src_num, dst_num):
    file_name = f"{src_num}-{dst_num}.out"
    buffer_size = 1e8
    buffer_dict = {}
    buffer_count = 0
    def flush_buffer():
        with lock:
            for (symbol, lines) in buffer_dict.items():
                with open(f"{args.out_dir}/{symbol}.out", "a") as dst:
                    dst.write("".join(lines))     
    with open(f"{blast_out_dir}/{file_name}", "r") as f:
        for line in f:
            row = line.strip().split("\t")
            query = row[0].strip()
            target = row[1].strip()
            symbols = []
            if query in refseq_to_symbols:
                symbols = symbols + refseq_to_symbols[query]
            if target in refseq_to_symbols:
                symbols = symbols + refseq_to_symbols[target]
            symbols = list(set(symbols)) # make unique
            for symbol in symbols:
                if symbol not in buffer_dict.keys():
                    buffer_dict[symbol] = []
                buffer_dict[symbol].append(f"{file_name}:{line}")
                buffer_count += 1
                if buffer_count >= buffer_size:
                    flush_buffer()
                    buffer_dict = {}
                    buffer_count = 0
    flush_buffer()

if __name__ == '__main__':
    main()
