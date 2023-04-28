from multiprocessing.pool import Pool
from multiprocessing import Lock, Manager
import os
import csv

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('query_symbol_list', action='store', type=str)
    parser.add_argument('--out_dir', action='store', type=str)
    parser.add_argument('--num_threads', action='store', type=int, default=48)
    args = parser.parse_args()
    if not os.path.isdir(args.out_dir):
        raise f"{args.out_dir} does not exist!"
    query_parallel(args.query_symbol_list, args.out_dir, args.num_threads)

def query(src_num, dst_num, protein_to_symbols, symbol_to_file, lock, target_dir):
    file_name = f"{src_num}-{dst_num}.out"
    print(f"Reading {file_name}...")
    flush_interval = 1e8
    buffered_lines = {}
    buffered_count = 0
    def flush():
        with lock:
            for (symbol, lines) in buffered_lines.items():
                with open(symbol_to_file[symbol], "a") as dst:
                    dst.write("".join(lines))     
    with open(f"/home/chiba/share/orth/blasting.homologene.2022-04/blast.out/{file_name}", "r") as f:
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
    print(f"Completed {file_name}!")

def query_parallel(symbol_list_path, target_dir, num_threads):
    with open(symbol_list_path, 'r') as f:
        symbol_list = f.read().strip().split('\n')
    manager = Manager()
    symbol_to_file = {}
    for symbol in symbol_list:
        symbol_to_file[symbol] = os.path.join(target_dir, symbol + '.out')
    protein_to_symbols = {}
    with open("/home/chiba/share/ncbi/gene/gene2refseq_tax9606", 'r') as f:
        for line in f:
            tokens = line.strip().split("\t")
            protein = tokens[5]
            symbol = tokens[15]
            if protein != '-' and symbol in symbol_to_file:
                if protein not in protein_to_symbols:
                    protein_to_symbols[protein] = []
                protein_to_symbols[protein].append(symbol)

    print("start pool")
    lock = manager.Lock()
    with Pool(processes=num_threads) as pool:
        for src_num in range(1, 22):
            pool.apply_async(query, args=(src_num, 1, protein_to_symbols, symbol_to_file, lock, target_dir))
        for dst_num in range(2, 22):
            pool.apply_async(query, args=(1, dst_num, protein_to_symbols, symbol_to_file, lock, target_dir))
        pool.close()
        pool.join()

if __name__ == '__main__':
    main()
