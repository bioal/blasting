from threading import Thread, Semaphore
import time
import subprocess
import os

class BlastManager:
    # constructor
    def __init__(self, command, num, db_list, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder) 
        self.output_folder = output_folder
        self.genome_list = self.__get_genome_list(db_list)
        self.semaphore = Semaphore(int(num))
        self.command = command

    # get list
    def __get_genome_list(self, db_list):
        fp = open(db_list, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 4:
                id = tokens[0]
                gcf_id = tokens[1]
                species = tokens[2]
                fasta_file = tokens[3]
                genome = {'id':id, 'gcf_id':gcf_id, 'species':species, 'fasta_file':fasta_file}
                list.append(genome)
        fp.close()
        return list

    # search
    def search(self):
        human = None
        for genome in self.genome_list:
            if int(genome['id']) == 1:
                human = genome

        for genome in self.genome_list:
            thread1 = Thread(target=self.__execute_blast, args=(genome, human))
            thread1.start()

            if not genome == human:
                thread2 = Thread(target=self.__execute_blast, args=(human, genome))
                thread2.start()

    def __execute_blast(self, genome1, genome2):
        with self.semaphore:
            output_file = self.output_folder + '/' + genome1['id'] + '-' + genome2['id']
            query = genome1['fasta_file']
            db = 'db/' + genome2['id']

            command = [
                self.command,
                '-query', query,
                '-db', db,
                '-max_target_seqs', '1',
                '-outfmt', '6',
                '-out', output_file
            ]
            command_line = ' '.join(command)
            print('Exec: ' + command_line)
            process = subprocess.Popen(command)
            process.wait()

