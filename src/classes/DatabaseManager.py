import subprocess
import os

class DatabaseManager:
    def __init__(self, genome_file_list, makedb, command):
        # if not os.path.exists(output_folder):
        #     os.makedirs(output_folder)
        self.list_dir = 'gene_lists'
        self.db_dir = 'blastdb'
        if not os.path.exists(self.list_dir):
            os.makedirs(self.list_dir)
        if makedb and not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        # self.output_folder = output_folder
        self.genome_list = self.__read_genome_list(genome_file_list)
        self.makedb = makedb
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
        fp = open('./dbs.txt', 'w')

        for genome in self.genome_list:
            id = genome['id']
            file = genome['file']
            species = genome['species']
            gene_id = genome['gene_id']

            gene_list_file = self.list_dir + '/' + id + '.txt'
            db = self.db_dir + '/' + id

            self.__make_list(file, gene_list_file)
            if self.makedb:
                self.__make_db(file, db)

            line = id + '\t' + gene_id + '\t' + species + '\t' + file + '\t' + gene_list_file + '\t' + db + '\n'
            fp.write(line)

        fp.close()

    # make list file
    def __make_list(self, faa_file, gene_list_file):
        in_fp = open(faa_file, 'r')
        out_fp = open(gene_list_file, 'w')

        count = 1
        for line in in_fp:
            if line.startswith('>'):
                line = line[1:].strip()
                out_fp.write(str(count) + '\t' + line + '\n')
                count = count + 1;
        in_fp.close()
        out_fp.close()


    # make blast db file
    def __make_db(self, faa_file, db):
        command = [
            self.command,
            '-dbtype',
            'prot',
            '-parse_seqids',
            '-in',
            faa_file,
            '-out',
            db
        ]
        print('Exec: ' + ' '.join(command))
        process = subprocess.Popen(command)
        process.wait()

