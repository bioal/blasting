import subprocess
import os

class DataManager:
    def __init__(self, proteome_file_list, command):
        self.proteins_dir = 'proteins'
        self.db_dir = 'db'
        if not os.path.exists(self.proteins_dir):
            os.makedirs(self.proteins_dir)
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        self.proteome_list = self.__read_proteome_list(proteome_file_list)
        self.command = command

    def __read_proteome_list(self, proteome_file_list):
        proteome_list = []
        fp = open(proteome_file_list, 'r')
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 2:
                proteome = { 'id': tokens[0], 'fasta_file': tokens[1] }
                proteome_list.append(proteome)
        fp.close()
        proteome_list.sort(key=lambda x: int(x['id']))
        return proteome_list

    def preprocess(self):
        for proteome in self.proteome_list:
            id = proteome['id']
            fasta_file = proteome['fasta_file']
            proteins_list = self.proteins_dir + '/' + id
            db = self.db_dir + '/' + id

            self.__make_proteins_list(fasta_file, proteins_list)
            self.__make_db(fasta_file, db)

    def __make_proteins_list(self, fasta_file, proteins_list):
        in_fp = open(fasta_file, 'r')
        out_fp = open(proteins_list, 'w')

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
            '-in', fasta_file,
            '-out', db,
            '-dbtype', 'prot',
            '-parse_seqids'
        ]
        subprocess.run(command)
