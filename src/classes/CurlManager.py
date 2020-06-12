import sys
import os
import datetime
import gzip
import subprocess
from ftplib import FTP
from dateutil import parser
from classes.FtpCli import FtpCli

class CurlManager:
    ftps = {}

    def __init__(self, server):
        self.server = server

        if server in CurlManager.ftps:
            self.ftp = CurlManager.ftps[server]
        else:
            self.ftp = self.__login()
            CurlManager.ftps[server] = self.ftp

    def download(self, path, output_file):
        if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
            command = ['curl', '-o', output_file, self.server + path]

            log_file = output_file + '.log'
            err_file = output_file + '.err'

            log_fp = open(log_file, 'w')
            err_fp = open(err_file, 'w')

            log_fp.write(' '.join(command) + '\n')
            ret = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log_fp.write(ret.stdout.decode())
            err_fp.write(ret.stderr.decode())

            log_fp.close()
            err_fp.close()

    def download_gz(self, path, output_file):
        unzip_file = output_file.replace('.gz', '')
        if not os.path.exists(unzip_file) or os.path.getsize(unzip_file) == 0:
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

    def __login(self):
        ftp = FTP(self.server)
        ftp.login('anonymous', '')
        return ftp

    def __write_line(fp, string):
        fp.write(string)
        fp.write('\n')
