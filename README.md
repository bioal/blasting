# hop

Python3

## Usage
    $ 1.download_gene_files.py -l species_list.tsv -o genome
    $ 2.make_database.py -l gene_files.txt -o database
    $ 3.blast_search.py -n 4 -l databases.txt -o blast
    $ 4.make_matrix.py -i blast -l databases.txt -o matrix
