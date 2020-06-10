import sys
from classes.FtpManager import FtpManager
from classes.CurlManager import CurlManager
import os
from threading import Thread, Semaphore

class ProteomeDownloader:
    def __init__(self, output_folder, species_list, num):
        self.ftp_server = 'ftp.uniprot.org'
        self.summary_file_source = '/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README'
        self.downloaded_files = 'proteome_list.tsv';
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder
        self.id_hash = self.__get_id_hash(species_list)
        self.taxid_hash = self.__get_taxid_hash(species_list)
        self.species_hash = self.__get_species_hash(species_list)
        self.cores = num
        self.semaphore = Semaphore(int(num))

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
        # ftp = CurlManager(self.ftp_server)
        ftp.download(self.summary_file_source, summary_file)
        self.__download_files(summary_file, debug)

    def __download_files(self, summary_file, debug):
        print('Downloading... files', file=sys.stderr, flush=True)
        file_obtained = {}
        fp = open(summary_file, 'r', encoding='UTF-8')
        line = fp.readline()
        threads = []
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
                    thread = Thread(name=gcf_id, target=self.__download_file, args=(url, debug, file_obtained, id))
                    threads.append(thread)
                    thread.start()
            line = fp.readline()
        fp.close()
        
        for t in threads:
            t.join()

        print('Downloading files done.', file=sys.stderr, flush=True)
        result_fp = open(self.downloaded_files, 'w')
        err_fp = open(self.downloaded_files + '.err', 'w')
        for id in self.id_hash:
            if file_obtained.get(id) is None:
                print(self.id_hash[id], file=err_fp)
            else:
                result_fp.write(id + '\t' + file_obtained[id] + '\n');
        result_fp.close()
        err_fp.close()
        print('Created', self.downloaded_files, file=sys.stderr, flush=True)
    
    def __download_file(self, url, debug, file_obtained, id):
        with self.semaphore:
            server = url.replace('ftp://', '')
            index = server.find('/')
            path = server[index:]
            server = server[0:index]
            if self.cores == 1:
                ftp = FtpManager(server)
            else:
                ftp = CurlManager(server)
            index = path.rfind('/')
            file_name = path[index + 1:]
            print(id + '\t' + self.output_folder + '/' + file_name.replace('fasta.gz', 'fasta'), flush=True)
            if not debug:
                ftp.download_gz(path, self.output_folder + '/' + file_name)
            file_obtained[id] = self.output_folder + '/' + file_name.replace('fasta.gz', 'fasta')
