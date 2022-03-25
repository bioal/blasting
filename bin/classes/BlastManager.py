from threading import Thread, Semaphore
import time
import subprocess
import os
import sys

class BlastManager:
    def __init__(self, command, num, organism_list, db_dir, out_dir):
        self.command = command
        self.semaphore = Semaphore(int(num))
        self.organisms = self.__read_organism_list(organism_list)
        self.db_dir = db_dir
        if not os.path.exists(out_dir):
            os.makedirs(out_dir) 
        self.out_dir = out_dir

    def __read_organism_list(self, organism_list):
        fp = open(organism_list, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                list.append({'id':tokens[0], 'fasta_file':tokens[1]})
        fp.close()
        return list

    def all_vs_all(self):
        for org1 in self.organisms:
            for org2 in self.organisms:
                thread1 = Thread(target=self.__execute_blast, args=(org1, org2))
                thread1.start()
                print('Queued ' + org1['id'] + '-' + org2['id'], flush=True)

    def search(self):
        human_info = None
        for org in self.organisms:
            if int(org['id']) == 1:
                human_info = org

        for org in self.organisms:
            thread1 = Thread(target=self.__execute_blast, args=(org, human_info))
            thread1.start()

            if not org == human_info:
                thread2 = Thread(target=self.__execute_blast, args=(human_info, org))
                thread2.start()

    def __execute_blast(self, org1, org2):
        with self.semaphore:
            query_file = org1['fasta_file']
            db_file = self.db_dir + '/' + org2['id']
            out_file = self.out_dir + '/' + org1['id'] + '-' + org2['id'] + '.out'
            log_file = self.out_dir + '/' + org1['id'] + '-' + org2['id'] + '.log'
            end_file = self.out_dir + '/' + org1['id'] + '-' + org2['id'] + '.end'
            if os.path.exists(end_file):
                print(f'Found {end_file}, skip', file=sys.stderr)
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
                with open(end_file, 'w') as end_fp:
                    end_fp.write(ret.stderr.decode())
                    end_fp.flush()
