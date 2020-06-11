import os
import datetime
import sys
import ftplib
import dateutil.parser

class FtpChecker:
    def __init__(self, server):
        self.ftp = ftplib.FTP(server, 'anonymous', '')

    def check_up_to_date(self, path):
        remote_size = self.ftp.size(path)
        remote_date = self.__get_remote_datetime(path)
        remote_utime = remote_date.timestamp()
        # print(path, remote_size, remote_date, remote_utime, sep='\t', flush=True)
        local_name = os.path.basename(path)
        if os.path.exists(local_name):
            local_size = os.path.getsize(local_name)
            local_utime = os.path.getmtime(local_name)
            local_datetime = datetime.datetime.fromtimestamp(local_utime)
            # print(local_name, local_size, local_datetime, local_utime)
            # os.utime(local_name, (remote_utime, remote_utime))
            if local_size == remote_size and local_datetime >= remote_date:
                return True
        return False

    def __get_remote_datetime(self, path):
        info = self.ftp.voidcmd(f'MDTM {path}')
        return dateutil.parser.parse(info[4:])

    def list(self, path):
        # outputs list to stdout
        # returns status
        self.ftp.retrlines(f'LIST {path}')

    def ls(self, path):
        print(self.ftp.nlst(path))

    def close(self):
        self.ftp.close()
