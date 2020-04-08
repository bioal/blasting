from classes.FtpManager import FtpManager
import os

# genome file downloader
class GenomeDownloader:
    # constructor
    def __init__(self, output_folder, species_list):
        self.ftp_server = 'ftp.ncbi.nlm.nih.gov'
        self.summary_file_source = '/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt'
        self.downloaded_genome_files = 'downloaded_genome_files.tsv';
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder
        self.hash = self.__get_hash(species_list)
        self.taxid_hash = self.__get_taxid_hash(species_list)
        self.species_hash = self.__get_species_hash(species_list)

    def __get_hash(self, species_list):
        hash = {}
        fp = open(species_list, 'r')
        line = fp.readline()
        while line:
            line = line.strip()
            tokens = line.split('\t')
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
        self.__download_genomes(summary_file, debug)

    def __download_genomes(self, summary_file, debug):
        result_fp = open(self.downloaded_genome_files, 'w')
        obtained = {}
        fp = open(summary_file, 'r', encoding='UTF-8')
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
                        gcf_file = self.__download_gcf_file(url)
                        result_fp.write(id + '\t' + gcf_id + '\t' + species + '\t' + gcf_file + '\n')
            line = fp.readline()
        fp.close()
        result_fp.close()
        if debug:
            for id in self.species_hash.values():
                if not obtained.get(id):
                    print(self.hash[id])
    
    def __download_gcf_file(self, url):
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
