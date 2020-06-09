import sys
import os
import datetime
import gzip
import subprocess
from ftplib import FTP
from dateutil import parser

# curl manager
class CurlManager:
    ftps = {}

    # constructor
    def __init__(self, server):
        self.server = server

        if server in CurlManager.ftps:
            self.ftp = CurlManager.ftps[server]
        else:
            self.ftp = self.__login()
            CurlManager.ftps[server] = self.ftp

    # downloads file 
    def download(self, path, output_file):
        if self.__check_file(path, output_file):
            print('Downloading... ' + path, file=sys.stderr)

            self.__call_curl(path, output_file)
        else:
            print('Skip... ' + path, file=sys.stderr)

    # call curl
    def __call_curl(self, path, output_file):
        log_file = output_file + '.log'
        err_file = output_file + '.err'

        command = [
            'curl',
            '-o', output_file,
            self.server + path
        ]

        log_fp = open(log_file, 'w')
        log_fp.write(' '.join(command) + '\n')
        ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_fp.write(ret.stdout.decode())
        log_fp.close()

        err_fp = open(err_file, 'w')
        err_fp.write(ret.stderr.decode())
        err_fp.close()

    
    # download gz
    def download_gz(self, path, output_file):
        unzip_file = output_file.replace('.gz', '')
        if self.__check_file(path, unzip_file):
            if os.path.exists(output_file):
                os.remove(output_file)
            if os.path.exists(unzip_file):
                os.remove(unzip_file)

            self.download(path, output_file)

            in_fp = gzip.open(output_file, 'rb')
            out_fp = open(unzip_file, 'wb')
            out_fp.write(in_fp.read())

            in_fp.close()
            out_fp.close()

            # os.remove(output_file)
        else:
            print('Skip... ' + path, file=sys.stderr)


    # list
    def list(self, path):
        files = self.ftp.nlst(path)
        return files

    # check file timestamp
    def __check_file(self, path, output_file):
        remote_info = self.ftp.voidcmd('MDTM ' + path)
        remote_time = parser.parse(remote_info[4:].strip())

        download_flag = True
        if os.path.exists(output_file):
            timestamp = datetime.datetime.fromtimestamp(os.stat(output_file).st_mtime)
            if os.path.getsize(output_file) > 0 and timestamp >= remote_time:

                download_flag = False

        return download_flag

    # login ftp
    def __login(self):
        ftp = FTP(self.server)
        ftp.login('anonymous', '')
        return ftp

    # writes line
    def __write_line(fp, string):
        fp.write(string)
        fp.write('\n')
    
