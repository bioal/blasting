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
protein_to_symbols = {}
with open(f"{ncbi_gene_dir}/gene2refseq_tax9606", 'r') as f:
    for line in f:
        tokens = line.strip().split("\t")
        protein = tokens[5]
        symbol = tokens[15]
        if protein != '-' and symbol in symbol_dict:
            if protein not in protein_to_symbols:
                protein_to_symbols[protein] = []
            protein_to_symbols[protein].append(symbol)

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
    flush_interval = 1e8
    buffered_lines = {}
    buffered_count = 0
    def flush():
        with lock:
            for (symbol, lines) in buffered_lines.items():
                with open(f"{args.out_dir}/{symbol}.out", "a") as dst:
                    dst.write("".join(lines))     
    with open(f"{blast_out_dir}/{file_name}", "r") as f:
        for line in f:
            row = line.strip().split("\t")
            query = row[0].strip()
            target = row[1].strip()
            symbols = []
            if query in protein_to_symbols:
                symbols = symbols + protein_to_symbols[query]
            if target in protein_to_symbols:
                symbols = symbols + protein_to_symbols[target]
            symbols = list(set(symbols)) # make unique
            for symbol in symbols:
                if symbol not in buffered_lines.keys():
                    buffered_lines[symbol] = []
                buffered_lines[symbol].append(f"{file_name}:{line}")
                buffered_count += 1
                if buffered_count % flush_interval == 0:
                    flush()
                    buffered_lines = {}
                    buffered_count = 0
    flush()

if __name__ == '__main__':
    main()
