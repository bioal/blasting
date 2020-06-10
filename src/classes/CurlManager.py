import sys
import os
import datetime
import gzip
import subprocess
from ftplib import FTP
from dateutil import parser

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
        if self.__check_file(path, output_file):
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
        # if self.__check_file(path, unzip_file):
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

    def list(self, path):
        files = self.ftp.nlst(path)
        return files

    def __check_file(self, path, output_file):
        remote_info = self.ftp.voidcmd('MDTM ' + path)
        remote_time = parser.parse(remote_info[4:].strip())

        download_flag = True
        if os.path.exists(output_file):
            timestamp = datetime.datetime.fromtimestamp(os.stat(output_file).st_mtime)
            if os.path.getsize(output_file) > 0 and timestamp >= remote_time:
                download_flag = False

        return download_flag

    def __login(self):
        ftp = FTP(self.server)
        ftp.login('anonymous', '')
        return ftp

    def __write_line(fp, string):
        fp.write(string)
        fp.write('\n')
