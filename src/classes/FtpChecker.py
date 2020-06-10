import os
import datetime
import sys
import ftplib
from dateutil import parser

class FtpChecker:
    def __init__(self, server):
        self.ftp = ftplib.FTP(server, 'anonymous', '')

    def check_file(self, path):
        remote_size = self.ftp.size(path)
        remote_info = self.ftp.voidcmd('MDTM ' + path)
        remote_stamp = parser.parse(remote_info[4:].strip())
        print(path, remote_size, remote_stamp, sep='\t', file=sys.stderr, flush=True)
        local_name = os.path.basename(path)
        local_size = os.path.getsize(local_name)
        local_stamp = os.stat(local_name).st_mtime
        local_date = datetime.datetime.fromtimestamp(local_stamp)
        print(local_name, local_size, local_date)

    def sendcmd(self, path):
        ret = self.ftp.sendcmd(path)
        print(ret)

    def nlst(self, path):
        print(self.ftp.nlst(path))

    def close(self):
        self.ftp.close()
