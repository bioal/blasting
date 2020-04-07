from classes.FtpManager import FtpManager
import os

# genome file downloader
class GenomeDownloader:
    # constructor
    def __init__(self, output_folder, list_file):
        self.ftp_server = 'ftp.ncbi.nlm.nih.gov'
        self.list_file_path = '/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt'
        self.list_file_name = 'assembly_summary_refseq.txt'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder
        self.id_list = self.__get_id_list(list_file)
        self.species_list = self.__get_species_list(list_file)

    # get id list
    def __get_id_list(self, list_file):
        list = {}
        fp = open(list_file, 'r')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if len(tokens) >= 7:
                list[tokens[5]] = tokens[0]
                list[tokens[6]] = tokens[0]
            line = fp.readline()
        fp.close()
        return list


    # get species list
    def __get_species_list(self, list_file):
        list = {}

        fp = open(list_file, 'r')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if len(tokens) >= 2:
                species = tokens[1]
                list[species] = tokens[0]
            line = fp.readline()
        fp.close()
        return list

    # download
    def download(self, debug):
        self.__download_list_file()
        self.__download_gene_files(debug)

    # downloads list file
    def __download_list_file(self):
        self.list_file = './' + self.list_file_name
        ftp = FtpManager(self.ftp_server)
        ftp.download(self.list_file_path, self.list_file)

    def __download_gene_files(self, debug):
        fp = open(self.list_file, 'r', encoding='UTF-8')
        result_fp = open('./gene_files.txt', 'w')
        line = fp.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                tokens = line.split('\t')
                if len(tokens) >= 8:
                    gene_id = tokens[0]
                    species = tokens[7]
                    url = None
                    id = None
                    if species in self.species_list:
                        id = self.species_list[species]
                    if gene_id in self.id_list:
                        id = self.id_list[gene_id]
                    if id is not None:
                        for token in tokens:
                            if token.startswith('ftp://'):
                                url = token
                    if url is not None:
                        if debug:
                            print(url)
                        else:
                            gene_file = self.__download_gene_file(gene_id, url)
                            result_fp.write(id + '\t' + gene_id + '\t' + species + '\t' + gene_file + '\n')
                        
            line = fp.readline()
        fp.close()
    
    def __download_gene_file(self, gene_id, url):
        server = url.replace('ftp://', '')
        index = server.find('/')
        path = server[index:]
        server = server[0:index]
        ftp = FtpManager(server)
        files = ftp.list(path)

        faa = None
        file_name = None
        for file in files:
            if file.endswith('faa.gz'):
                faa = file
        if faa is not None:
            index = faa.rfind('/')
            file_name = faa[index + 1:]
            faa_file = self.output_folder + '/' + file_name
            ftp.download_gz(faa, faa_file)
            file_name = file_name.replace('faa.gz', 'faa')
        return self.output_folder + '/' + file_name
