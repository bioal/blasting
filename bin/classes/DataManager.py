import subprocess
import os

class DataManager:
    def __init__(self, genome_file_list, command, genes_dir, db_dir):
        self.genes_dir = genes_dir
        self.db_dir = db_dir
        if not os.path.exists(self.genes_dir):
            os.makedirs(self.genes_dir)
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        self.genome_list = self.__read_genome_list(genome_file_list)
        self.command = command

    def __read_genome_list(self, genome_file_list):
        genome_list = []
        fp = open(genome_file_list, 'r')
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                genome = { 'id': tokens[0], 'fasta_file': tokens[1] }
                genome_list.append(genome)
        fp.close()
        genome_list.sort(key=lambda x: int(x['id']))
        return genome_list

    def preprocess(self):
        for genome in self.genome_list:
            no = genome['id']
            fasta_file = genome['fasta_file']
            self.__make_genes_list(fasta_file, f'{self.genes_dir}/{no}')
        for genome in self.genome_list:
            no = genome['id']
            fasta_file = genome['fasta_file']
            subprocess.run(f'{self.command} -in {fasta_file} -out {self.db_dir}/{no} -dbtype prot -parse_seqids >> {self.db_dir}.log', shell=True)

    def __make_genes_list(self, fasta_file, genes_list):
        in_fp = open(fasta_file, 'r')
        out_fp = open(genes_list, 'w')
        count = 1
        for line in in_fp:
            if line.startswith('>'):
                line = line[1:].strip()
                out_fp.write(str(count) + '\t' + line + '\n')
                count = count + 1;
        in_fp.close()
        out_fp.close()
