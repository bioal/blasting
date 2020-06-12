#!/usr/bin/env python3
import argparse
from classes.FtpCli import FtpCli

parser = argparse.ArgumentParser(description='submit FTP command')
parser.add_argument('path', help='file path on the server')
args = parser.parse_args()

path = args.path.replace('ftp://', '')
pos = path.find('/')
server = path[0:pos]
path = path[pos:]

print(f'server: {server}')
print(f'path: {path}')

cli = FtpCli(server)

if cli.check_up_to_date(path):
    print('status: up to date')
else:
    print('status: obsolete')

cli.close()
