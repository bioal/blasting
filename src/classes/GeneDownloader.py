from classes.FtpManager import FtpManager

# gene file downloader
class GeneDownloader:
    # constructor
    def __init__(self, output_folder):
        self.ftp_server = 'ftp.ncbi.nlm.nih.gov'
        self.list_file_path = '/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt'
        self.list_file_name = 'assembly_summary_refseq.txt'
        self.output_folder = output_folder

    # download
    def download(self):
        self.__download_list_file()
        self.__download_gene_files()

    # downloads list file
    def __download_list_file(self):
        self.list_file = self.output_folder + '/' + self.list_file_name
        ftp = FtpManager(self.ftp_server)
        ftp.download(self.list_file_path, self.list_file)

    # downloads gene files
    def __download_gene_files(self):
        fp = open(self.list_file, 'r', encoding='UTF-8')
        line = fp.readline()
        while line:
            line = line.strip()
            if not line.startswith('#'):
                tokens = line.split('\t')
                if len(tokens) >= 0:
                    gene_id = tokens[0]
                    url = None
                    for token in tokens:
                        if token.startswith('ftp://'):
                            url = token
                    if not url == None:
                        self.__download_gene_file(gene_id, url)
            line = fp.readline()
        fp.close()
    
    # download gene file
    def __download_gene_file(self, gene_id, url):
        server = url.replace('ftp://', '')
        index = server.find('/')
        path = server[index:]
        server = server[0:index]
        ftp = FtpManager(server)
        files = ftp.list(path)

        faa = None
        for file in files:
            if file.endswith('faa.gz'):
                faa = file
        if not faa == None:
            index = faa.rfind('/')
            faa_file = self.output_folder + '/' + faa[index + 1:]
            ftp.download_binary(faa, faa_file)
