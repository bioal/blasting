# hop

## Usage
    $ download_gene_files.py -l species_list.tsv -o genome
    $ make_database.py -l gene_files.txt -o database
    $ blast_search.py -n 4 -l databases.txt -o blast
    $ make_matrix.py -i blast -l databases.txt -o matrix
