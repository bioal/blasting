import os
import sys
import re
from threading import Thread, Semaphore
from classes.FtpCli import FtpCli
from classes.SpeciesManager import SpeciesManager

class GenomeDownloader:
    def __init__(self, out_dir, num):
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        self.out_dir = out_dir
        self.semaphore = Semaphore(int(num))

    def download_summary_file(self, ftp_server, summary_file_source, dir):
        index = summary_file_source.rfind('/')
        summary_file = dir + summary_file_source[index + 1:]
        
        ftp = FtpCli(ftp_server)
        if not ftp.is_up_to_date(summary_file_source, summary_file):
            ftp.get(summary_file_source, summary_file)
        ftp.close()
        
        return summary_file

    def sync(self, genomes_found, success_file, err_file, debug):
        fp = open(genomes_found, 'r', encoding='UTF-8')
        result_fp = open(success_file, 'w')
        for line in fp:
            line = line.rstrip()
            fields = line.split('\t')
            id = fields[0]
            url = fields[20]
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
            outfile = self.out_dir + '/' + gz_file_name
            ftp = FtpCli(server)
            ftp.sync(gz_file_path, outfile)
            ftp.close()
            print(id + '\t' + re.sub(r'.gz', '', outfile), file=result_fp, flush=True)
        fp.close()
        result_fp.close()

    def download_files(self, summary_file, species_list, success_file, err_file, debug):
        file_obtained = {}
        threads = []
        sp = SpeciesManager(species_list);
        fp = open(summary_file, 'r', encoding='UTF-8')
        for line in fp:
            line = line.rstrip()
            fields = line.split('\t')
            if not line.startswith('#') and len(fields) >= 8:
                gcf_id = fields[0]
                taxid = fields[5]
                species_taxid = fields[6]
                species = fields[7]
                url = fields[19]
                id = sp.species.get(species) or \
                     sp.taxids.get(taxid) or \
                     sp.taxids.get(species_taxid)
                if id is not None and file_obtained.get(id) is None:
                    t = Thread(name=gcf_id, target=self.__download_file, args=(url, debug, file_obtained, id))
                    threads.append(t)
                    t.start()
        fp.close()

        for t in threads:
            t.join()

        result_fp = open(success_file, 'w')
        err_fp = open(err_file, 'w')
        count = 0
        count_fail = 0
        count_success = 0
        for id in sp.ids:
            count += 1
            if file_obtained.get(id) is None:
                print(sp.ids[id], file=err_fp)
                count_fail += 1
            else:
                print(id + '\t' + file_obtained[id], file=result_fp);
                count_success += 1
        result_fp.close()
        err_fp.close()
        print(f'Tried {count} genomes, {count_success} succeeded, {count_fail} failed.')
        if count:
            message = 'Created'
            if count_success:
                message += ' ' + success_file
            if count_fail:
                message += ' ' + err_file
            print(message, file=sys.stderr, flush=True)
        if not os.path.getsize(success_file):
            os.remove(success_file)
        if not os.path.getsize(err_file):
            os.remove(err_file)

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
            outfile = self.out_dir + '/' + gz_file_name
            print(f'{id}\t{outfile}', flush=True)
            if not debug:
                ftp = FtpCli(server)
                if not ftp.is_up_to_date(gz_file_path, outfile):
                    ftp.get(gz_file_path, outfile)
                ftp.close()
            file_obtained[id] = re.sub(r'.gz', '', outfile)
