from threading import Thread, Semaphore
import time
import subprocess
import os

class BlastManager:
    def __init__(self, command, num, genome_list, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder) 
        self.output_folder = output_folder
        self.genome_list = self.__read_genome_list(genome_list)
        self.semaphore = Semaphore(int(num))
        self.command = command
        self.err_dir = output_folder + '_err'
        self.log_dir = output_folder + '_log'
        if not os.path.exists(self.err_dir):
            os.makedirs(self.err_dir)
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

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
            result_name = genome1['id'] + '-' + genome2['id']
            log_file = self.log_dir + '/' + result_name
            err_file = self.err_dir + '/' + result_name
            if os.path.exists(err_file):
                return
            command = [
                self.command,
                '-query', genome1['fasta_file'],
                '-db', 'db/' + genome2['id'],
                # '-max_target_seqs', '1',
                '-evalue', '0.001',
                # '-outfmt', '6',
                '-outfmt', '7',
                '-out', self.output_folder + '/' + result_name
            ]
            log_fp = open(log_file, 'w')
            log_fp.write(' '.join(command) + '\n')
            log_fp.flush()
            ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log_fp.write(ret.stdout.decode())
            log_fp.close()
            err_fp = open(err_file, 'w')
            err_fp.write(ret.stderr.decode())
            err_fp.close()
