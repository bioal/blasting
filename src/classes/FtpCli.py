import os
import datetime
import sys
import ftplib
import gzip
import dateutil.parser

class FtpCli:
    def __init__(self, server):
        self.ftp = ftplib.FTP(server, 'anonymous', '')

    def is_up_to_date(self, path, local_name):
        remote_size = self.ftp.size(path)
        remote_date = self.__get_remote_datetime(path)
        remote_utime = remote_date.timestamp()
        if not os.path.exists(local_name):
            return False
        local_size = os.path.getsize(local_name)
        local_utime = os.path.getmtime(local_name)
        local_datetime = datetime.datetime.fromtimestamp(local_utime)
        flg = True
        if not local_size == remote_size:
            flg = False
            print(f'{local_name} size {local_size} != remote {remote_size}', file=sys.stderr, flush=True)
        if not local_datetime == remote_date:
            flg = False
            print(f'{local_datetime} != remote {remote_date}', file=sys.stderr, flush=True)
        # print(f'{local_name} is up to date', file=sys.stderr, flush=True)
        return flg

    def get(self, remote_path, outfile):
        remote_size = self.ftp.size(remote_path)
        remote_date = self.__get_remote_datetime(remote_path)
        remote_utime = remote_date.timestamp()
        fp = open(outfile, 'wb')
        self.ftp.retrbinary(f'RETR {remote_path}', fp.write)
        fp.close()
        if os.path.exists(outfile):
            local_size = os.path.getsize(outfile)
            if remote_size == local_size:
                os.utime(outfile, (remote_utime, remote_utime))
                if outfile.endswith('.gz'):
                    unzip_file = outfile.replace('.gz', '')
                    self.gz(outfile, unzip_file)
                    os.utime(unzip_file, (remote_utime, remote_utime))
            else:
                print(f'{outfile} size {local_size} != remote {remote_size}', file=sys.stderr)
        else:
            print(f'{outfile} not downloaded', file=sys.stderr)

    def gz(self, file, unzip_file):
        in_fp = gzip.open(file, 'rb')
        out_fp = open(unzip_file, 'wb')
        out_fp.write(in_fp.read())
        in_fp.close()
        out_fp.close()

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
