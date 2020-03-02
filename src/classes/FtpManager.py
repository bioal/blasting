import os
import datetime
from ftplib import FTP
from dateutil import parser
from classes.TxtFile import TxtFile

# FTP manager
class FtpManager:
    ftps = {}

    # constructor
    def __init__(self, server):
        self.server = server

        if server in FtpManager.ftps:
            self.ftp = FtpManager.ftps[server]
        else:
            self.ftp = self.__login()
            FtpManager.ftps[server] = self.ftp

    # downloads file 
    def download(self, path, output_file):
        if self.__check_file(path, output_file):
            print('Downloading... ' + path)
            fp = open(output_file, 'w', encoding='UTF-8')
            txt_file = TxtFile(fp)
            self.ftp.retrlines('RETR ' + path, txt_file.write_line)
            fp.close()
        else:
            print('Skip... ' + path)
    
    # download binary
    def download_binary(self, path, output_file):
        if self.__check_file(path, output_file):
            print('Downloading... ' + path)
            fp = open(output_file, 'wb')
            self.ftp.retrbinary('RETR ' + path, fp.write)
            fp.close()
        else:
            print('Skip... ' + path)

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
    
