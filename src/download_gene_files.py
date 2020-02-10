from functions import download

server = 'ftp.ncbi.nlm.nih.gov'
file = '/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt'

download(server, file, 'assermbly_summary_refseq.txt')
