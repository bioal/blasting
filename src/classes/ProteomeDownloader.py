from classes.FtpManager import FtpManager
import os

class ProteomeDownloader:
    def __init__(self, output_folder, species_list):
        self.ftp_server = 'ftp.uniprot.org'
        self.summary_file_source = '/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README'
        self.downloaded_proteomes = 'proteome_list.tsv';
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder
        self.id_hash = self.__get_id_hash(species_list)
        self.taxid_hash = self.__get_taxid_hash(species_list)
        self.species_hash = self.__get_species_hash(species_list)

    def __get_id_hash(self, species_list):
        hash = {}
        fp = open(species_list, 'r')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if tokens[0].isdigit():
                hash[tokens[0]] = line
            line = fp.readline()
        fp.close()
        return hash

    def __get_taxid_hash(self, species_list):
        hash = {}
        fp = open(species_list, 'r')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if len(tokens) >= 7:
                hash[tokens[6]] = tokens[0]
            line = fp.readline()
        fp.close()
        return hash

    def __get_species_hash(self, species_list):
        hash = {}

        fp = open(species_list, 'r')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if len(tokens) >= 2:
                species = tokens[1]
                hash[species] = tokens[0]
            line = fp.readline()
        fp.close()
        return hash

    def download(self, debug):
        index = self.summary_file_source.rfind('/')
        summary_file = self.summary_file_source[index + 1:]
        ftp = FtpManager(self.ftp_server)
        ftp.download(self.summary_file_source, summary_file)
        self.__download_proteomes(summary_file, debug)

    def __download_proteomes(self, summary_file, debug):
        file_obtained = {}
        fp = open(summary_file, 'r', encoding='UTF-8')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
            if line.startswith('UP000') and len(tokens) >= 8:
                gcf_id = tokens[0]
                taxid = tokens[1]
                species_taxid = tokens[1]
                species = tokens[7]
                url = 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/' + gcf_id + '_' + taxid + '.fasta.gz'
                id = self.species_hash.get(species) or \
                     self.taxid_hash.get(taxid) or \
                     self.taxid_hash.get(species_taxid)
                if id is not None and file_obtained.get(id) is None:
                    gcf_file = self.__download_gcf_file(url, debug)
                    file_obtained[id] = gcf_file
            line = fp.readline()
        fp.close()

        result_fp = open(self.downloaded_proteomes, 'w')
        for id in self.id_hash:
            if file_obtained.get(id) is None:
                print('Proteome not obtained for: ' + self.id_hash[id])
            else:
                result_fp.write(id + '\t' + file_obtained[id] + '\n');
        result_fp.close()
    
    def __download_gcf_file(self, url, debug):
        server = url.replace('ftp://', '')
        index = server.find('/')
        path = server[index:]
        server = server[0:index]
        ftp = FtpManager(server)
        files = ftp.list(path)

        faa = None
        gcf_file_path = None
        for file in files:
            if file.endswith('fasta.gz'):
                faa = file
        if faa is not None:
            index = faa.rfind('/')
            file_name = faa[index + 1:]
            faa_file = self.output_folder + '/' + file_name
            if not debug:
                ftp.download_gz(faa, faa_file)
            gcf_file_name = file_name.replace('fasta.gz', 'fasta')
            gcf_file_path = self.output_folder + '/' + gcf_file_name
        return gcf_file_path
