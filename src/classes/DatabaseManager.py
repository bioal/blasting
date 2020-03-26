import subprocess
import os

class DatabaseManager:
    # constructor
    def __init__(self, output_folder, list_file, command):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder
        self.list_file = self.__read_list_file(list_file)
        self.command = command


    # read list file
    def __read_list_file(self, list_file):
        fp = open(list_file, 'r')
        list = []
        for line in fp:
            tokens = line.strip().split('\t')
            if len(tokens) >= 4:
                genome = { 'id': tokens[0], 'gene_id': tokens[1], 'species': tokens[2], 'file': tokens[3] }
                list.append(genome)
        fp.close()
        list.sort(key=lambda x: int(x['id']))
        return list

    # make database
    def make_database(self):
        fp = open('./databases.txt', 'w')

        database_dir = self.output_folder + '/database'
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)
        list_dir = self.output_folder + '/gene_list'
        if not os.path.exists(list_dir):
            os.makedirs(list_dir)

        for genome in self.list_file:
            id = genome['id']
            file = genome['file']
            species = genome['species']
            gene_id = genome['gene_id']

            list_file = list_dir + '/' + id + '.txt'
            database = database_dir + '/' + id

            self.__make_list(file, list_file)
            self.__make_db(file, database)

            line = id + '\t' + gene_id + '\t' + species + '\t' + file + '\t' + list_file + '\t' + database + '\n'
            fp.write(line)

        fp.close()

    # make list file
    def __make_list(self, faa_file, list_file):
        in_fp = open(faa_file, 'r')
        out_fp = open(list_file, 'w')

        count = 1
        for line in in_fp:
            if line.startswith('>'):
                line = line[1:].strip()
                out_fp.write(str(count) + '\t' + line + '\n')
                count = count + 1;
        in_fp.close()
        out_fp.close()


    # make db file
    def __make_db(self, faa_file, database):
        command = [
            self.command,
            '-dbtype',
            'prot',
            '-parse_seqids',
            '-in',
            faa_file,
            '-out',
            database
        ]
        print('Exec: ' + ' '.join(command))
        process = subprocess.Popen(command)
        process.wait()

