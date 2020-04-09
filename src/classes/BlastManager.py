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

    def __read_genome_list(self, genome_list):
        fp = open(genome_list, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                list.append({'id':tokens[0], 'fasta_file':tokens[1]})
        fp.close()
        return list

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
            command = [
                self.command,
                '-query', genome1['fasta_file'],
                '-db', 'db/' + genome2['id'],
                '-max_target_seqs', '1',
                '-outfmt', '6',
                '-out', self.output_folder + '/' + genome1['id'] + '-' + genome2['id']
            ]
            print('Exec: ' + ' '.join(command))
            process = subprocess.Popen(command)
            process.wait()
