from threading import Thread, Semaphore
import time
import subprocess
import os

class BlastManager:
    # constructor
    def __init__(self, output_folder, db_list, num, command):
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
            if len(tokens) >= 6:
                id = tokens[0]
                gcf_id = tokens[1]
                species = tokens[2]
                faa_file = tokens[3]
                genes_file = tokens[4]
                db = tokens[5]
                
                genome = {'id':id, 'gcf_id':gcf_id, 'species':species, 'faa_file':faa_file, 'genes_file': genes_file, 'db': db}
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


    # blast
    def __execute_blast(self, genome1, genome2):
        with self.semaphore:
            output_file = self.output_folder + '/' + genome1['id'] + '-' + genome2['id'] + '.txt'
            db = genome2['db']
            query = genome1['faa_file']

            command = [
                self.command,
                '-db',
                db,
                '-query',
                query,
                '-max_target_seqs', '1',
                '-outfmt',
                '6',
                '-out',
                output_file
            ]
            command_line = ' '.join(command)
            print('Exec: ' + command_line)
            process = subprocess.Popen(command)
            process.wait()

