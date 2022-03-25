from threading import Thread, Semaphore
import time
import subprocess
import os
import sys

class BlastManager:
    def __init__(self, command, num, genome_list, db_dir, out_dir):
        self.command = command
        self.semaphore = Semaphore(int(num))
        self.genome_list = self.__read_genome_list(genome_list)
        self.db_dir = db_dir
        if not os.path.exists(out_dir):
            os.makedirs(out_dir) 
        self.out_dir = out_dir

    def __read_genome_list(self, genome_list):
        fp = open(genome_list, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                list.append({'id':tokens[0], 'fasta_file':tokens[1]})
        fp.close()
        return list

    def all_vs_all(self):
        for genome1 in self.genome_list:
            for genome2 in self.genome_list:
                thread1 = Thread(target=self.__execute_blast, args=(genome1, genome2))
                thread1.start()
                print(genome1['id'] + '-' + genome2['id'], flush=True)

    def search(self):
        human_genome = None
        for genome in self.genome_list:
            if int(genome['id']) == 1:
                human_genome = genome

        for genome in self.genome_list:
            thread1 = Thread(target=self.__execute_blast, args=(genome, human_genome))
            thread1.start()

            if not genome == human_genome:
                thread2 = Thread(target=self.__execute_blast, args=(human_genome, genome))
                thread2.start()

    def __execute_blast(self, genome1, genome2):
        with self.semaphore:
            query_file = genome1['fasta_file']
            db_file = self.db_dir + '/' + genome2['id']
            out_file = self.out_dir + '/' + genome1['id'] + '-' + genome2['id'] + '.out'
            log_file = self.out_dir + '/' + genome1['id'] + '-' + genome2['id'] + '.start'
            err_file = self.out_dir + '/' + genome1['id'] + '-' + genome2['id'] + '.end'
            if os.path.exists(err_file):
                print(f'Found {err_file}, skip', file=sys.stderr)
                return
            command = [ self.command, '-query', query_file, '-db', db_file, '-out', out_file,
                # '-max_target_seqs', '1',
                '-evalue', '0.001',
                # '-outfmt', '6',
                '-outfmt', '7'
            ]
            with open(log_file, 'w') as log_fp:
                print(' '.join(command), file=log_fp, flush=True)
                ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                log_fp.write(ret.stdout.decode())
                log_fp.flush()
                with open(err_file, 'w') as err_fp:
                    err_fp.write(ret.stderr.decode())
                    err_fp.flush()
