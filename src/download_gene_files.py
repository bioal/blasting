from classes.GeneDownloader import GeneDownloader

data_folder = '/opt/orthology/data/genome/tmp'
list_file = '/opt/orthology/data/species_list.tsv'

downloader = GeneDownloader(data_folder, list_file)
downloader.download()
