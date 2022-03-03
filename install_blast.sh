#!/bin/sh

mkdir -p lib
cd lib

curl -LOR ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.12.0/ncbi-blast-2.12.0+-x64-linux.tar.gz
curl -LOR ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.12.0/ncbi-blast-2.12.0+-x64-linux.tar.gz.md5
md5sum -c ncbi-blast-2.12.0+-x64-linux.tar.gz.md5

tar -zxvf ncbi-blast-2.12.0+-x64-linux.tar.gz
ln -s ncbi-blast-2.12.0+ blast
