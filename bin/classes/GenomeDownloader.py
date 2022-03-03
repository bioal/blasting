import os
import sys
import re
from threading import Thread, Semaphore
from classes.FtpCli import FtpCli
from classes.SpeciesManager import SpeciesManager

class GenomeDownloader:
    def __init__(self, output_folder, num):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.output_folder = output_folder
        self.semaphore = Semaphore(int(num))

    def download_summary_file(self, ftp_server, summary_file_source, dir):
        index = summary_file_source.rfind('/')
        summary_file = dir + summary_file_source[index + 1:]
        
        ftp = FtpCli(ftp_server)
        if not ftp.is_up_to_date(summary_file_source, summary_file):
            ftp.get(summary_file_source, summary_file)
        ftp.close()
        
        return summary_file

    def download_files(self, summary_file, species_list, downloaded_files, debug):
        file_obtained = {}
        threads = []
        species_man = SpeciesManager(species_list);
        fp = open(summary_file, 'r', encoding='UTF-8')
        for line in fp:
            line = line.strip()
            tokens = line.split('\t')
            if not line.startswith('#') and len(tokens) >= 8:
                gcf_id = tokens[0]
                taxid = tokens[5]
                species_taxid = tokens[6]
                species = tokens[7]
                url = tokens[19]
                id = species_man.species.get(species) or \
                     species_man.taxids.get(taxid) or \
                     species_man.taxids.get(species_taxid)
                if id is not None and file_obtained.get(id) is None:
                    thread = Thread(name=gcf_id, target=self.__download_file, args=(url, debug, file_obtained, id))
                    threads.append(thread)
                    thread.start()
        fp.close()

        for t in threads:
            t.join()

        print('Downloading done.', file=sys.stderr, flush=True)
        result_fp = open(downloaded_files, 'w')
        err_fp = open(downloaded_files + '.err', 'w')
        for id in species_man.ids:
            if file_obtained.get(id) is None:
                print(species_man.ids[id], file=err_fp)
            else:
                result_fp.write(id + '\t' + file_obtained[id] + '\n');
        result_fp.close()
        err_fp.close()
        print('Created', downloaded_files, file=sys.stderr, flush=True)

    def __download_file(self, url, debug, file_obtained, id):
        with self.semaphore:
            server = url.replace('ftp://', '')
            server = url.replace('https://', '')
            index = server.find('/')
            path = server[index:]
            server = server[0:index]
            index = path.rfind('/')
            name = path[index + 1:]
            if name.endswith('gz'):
                gz_file_name = name
                gz_file_path = path
            else:
                gz_file_name = name + '_protein.faa.gz'
                gz_file_path = f'{path}/{gz_file_name}'
            outfile = self.output_folder + '/' + gz_file_name
            print(f'{id}\t{outfile}', flush=True)
            if not debug:
                ftp = FtpCli(server)
                if not ftp.is_up_to_date(gz_file_path, outfile):
                    ftp.get(gz_file_path, outfile)
                ftp.close()
            file_obtained[id] = re.sub(r'.gz', '', outfile)
