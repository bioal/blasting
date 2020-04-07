from classes.FtpManager import FtpManager
import os

# genome file downloader
class GenomeDownloader:
    # constructor
    def __init__(self, output_folder, species_list):
        self.ftp_server = 'ftp.ncbi.nlm.nih.gov'
        self.list_file_path = '/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt'
        self.list_file_name = 'assembly_summary_refseq.txt'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder
        self.taxid_hash = self.__get_taxid_hash(species_list)
        self.species_hash = self.__get_species_hash(species_list)

    # get id list
    def __get_taxid_hash(self, list_file):
        list = {}
        fp = open(list_file, 'r')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if len(tokens) >= 7:
                list[tokens[6]] = tokens[0]
            line = fp.readline()
        fp.close()
        return list


    # get species list
    def __get_species_hash(self, list_file):
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
        obtained = {}
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if not line.startswith('#') and len(tokens) >= 8:
                gcf_id = tokens[0]
                taxid = tokens[5]
                species_taxid = tokens[6]
                species = tokens[7]
                url = None
                # id = None
                # if species in self.species_hash:
                #     id = self.species_hash[species]
                # if taxid in self.taxid_hash:
                #     id = self.taxid_hash[taxid]
                # if species_taxid in self.taxid_hash:
                #     id = self.taxid_hash[species_taxid]
                id = self.species_hash.get(species) or \
                     self.taxid_hash.get(taxid) or \
                     self.taxid_hash.get(species_taxid)
                if id is not None and obtained.get(id) is None:
                    for token in tokens:
                        if token.startswith('ftp://'):
                            url = token
                            obtained[id] = True
                if url is not None:
                    if debug:
                        print(id + '\t' + url)
                    else:
                        gene_file = self.__download_gene_file(gcf_id, url)
                        result_fp.write(id + '\t' + gcf_id + '\t' + species + '\t' + gene_file + '\n')
            line = fp.readline()
        fp.close()
        if debug:
            for id in self.species_hash.values():
                if not obtained.get(id):
                    print(id)
    
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
