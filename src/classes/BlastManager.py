from threading import Thread, Semaphore
import time
import subprocess

class BlastManager:
    # constructor
    def __init__(self, output_folder, list_file):
        self.output_folder = output_folder
        self.list_file = list_file
        index = list_file.rfind('/')
        if index < 0:
            self.data_folder = '.'
        else:
            self.data_folder = list_file[0:index]
        self.semaphore = Semaphore(4)
        self.command = '/opt/packages/blast/ncbi-blast-2.10.0+-src/c++/ReleaseMT/bin/blastp'

    # search
    def search(self):
        list = self.__get_gene_list()
        self.gene_list = list 
        for i in range(len(self.gene_list)):
            gene1 = self.gene_list[i]
            for j in range(i + 1, len(self.gene_list)):
                gene2 = self.gene_list[j]
                thread = Thread(target=self.__execute_blast, args=(gene1, gene2))
                thread.start()

    # get gene list
    def __get_gene_list(self):
        fp = open(self.list_file, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 3:
                gene = {'id':tokens[0], 'species':tokens[1], 'file':tokens[2]}
                list.append(gene)
        fp.close()
        return list

    # blast
    def __execute_blast(self, gene1, gene2):
        with self.semaphore:
            output_file = self.output_folder + '/' + gene1['id'] + '-' + gene2['id'] + '.txt'
            faa_file1 = self.data_folder + '/' + gene1['file']
            faa_file2 = self.data_folder + '/' + gene2['file']
            
            command_line = self.command + ' -query ' + faa_file1 + ' -subject ' + faa_file2 + ' -out ' + output_file
            print('Execute: ' + command_line)
            process = subprocess.Popen(command_line.strip().split(' '))
            process.wait()
            print('Done: ' + command_line)

