import subprocess
import os

class DataManager:
    def __init__(self, genome_file_list, command):
        self.list_dir = 'genes_lists'
        self.db_list = 'dbs.tsv'
        self.db_dir = 'db'
        if not os.path.exists(self.list_dir):
            os.makedirs(self.list_dir)
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        self.genome_list = self.__read_genome_list(genome_file_list)
        self.command = command

    def __read_genome_list(self, genome_file_list):
        genome_list = []
        fp = open(genome_file_list, 'r')
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 4:
                genome = { 'id': tokens[0], 'gene_id': tokens[1], 'species': tokens[2], 'file': tokens[3] }
                genome_list.append(genome)
        fp.close()
        genome_list.sort(key=lambda x: int(x['id']))
        return genome_list

    def preprocess(self):
        fp = open(self.db_list, 'w')

        for genome in self.genome_list:
            id = genome['id']
            file = genome['file']
            species = genome['species']
            gene_id = genome['gene_id']

            genes_list = self.list_dir + '/' + id
            db = self.db_dir + '/' + id

            self.__make_genes_list(file, genes_list)
            self.__make_db(file, db)

            line = id + '\t' + gene_id + '\t' + species + '\t' + file + '\t' + genes_list + '\t' + db + '\n'
            fp.write(line)

        fp.close()

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

    def __make_db(self, fasta_file, db):
        command = [
            self.command,
            '-dbtype',
            'prot',
            '-parse_seqids',
            '-in',
            fasta_file,
            '-out',
            db
        ]
        print('Exec: ' + ' '.join(command))
        process = subprocess.Popen(command)
        process.wait()

