from threading import Thread, Semaphore
import time
import subprocess
import os
import sys

class BlastManager:
    def __init__(self, command, num, organism_list, db_dir, out_dir):
        self.command = command
        self.semaphore = Semaphore(int(num))
        self.organisms, self.get_fasta = self.__read_organism_list(organism_list)
        self.db_dir = db_dir
        if not os.path.exists(out_dir):
            os.makedirs(out_dir) 
        self.out_dir = out_dir

    def __read_organism_list(self, organism_list):
        fp = open(organism_list, 'r')
        list = []
        get_fasta = {}
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                no = tokens[0]
                file_path = tokens[1]
                list.append(no)
                get_fasta[no] = file_path
        fp.close()
        return list, get_fasta

    def all_vs_all(self):
        for org1 in self.organisms:
            for org2 in self.organisms:
                thread1 = Thread(target=self.__execute_blast, args=(org1, org2))
                thread1.start()
                print(f'Queued {org1}-{org2}', flush=True)

    def exec_pairs(self, pairs_file):
        fp = open(pairs_file, 'r')
        for line in fp:
            fields = line.rstrip('\n').split('\t')
            org1 = fields[0]
            org2 = fields[1]
            thread1 = Thread(target=self.__execute_blast, args=(org1, org2))
            thread1.start()
            print(f'Queued {org1}-{org2}', flush=True)
        fp.close()

    def __execute_blast(self, org1, org2):
        with self.semaphore:
            start = time.time()
            query_file = self.get_fasta[org1]
            db_file = f'{self.db_dir}/{org2}'
            out_file = f'{self.out_dir}/{org1}-{org2}.out'
            log_file = f'{self.out_dir}/{org1}-{org2}.log'
            end_file = f'{self.out_dir}/{org1}-{org2}.end'
            if os.path.exists(end_file):
                print(f'Found {end_file}, skip', file=sys.stderr)
                return
            command = [ self.command, '-query', query_file, '-db', db_file, '-out', out_file,
                # '-max_target_seqs', '1',
                '-evalue', '0.01',
                # '-evalue', '0.001',
                # '-outfmt', '6',
                # '-outfmt', '6 std qlen slen',
                '-outfmt', '6 std qlen slen stitle',
                # '-outfmt', '7'
            ]
            with open(log_file, 'w') as log_fp:
                print(' '.join(command), file=log_fp, flush=True)
                ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                diff_time = (time.time() - start) / 3600
                log_fp.write(ret.stdout.decode())
                log_fp.flush()
                with open(end_file, 'w') as end_fp:
                    end_fp.write(ret.stderr.decode())
                    print(f'time: {diff_time:.4f} hours', file=end_fp, flush=True)
                    end_fp.flush()
