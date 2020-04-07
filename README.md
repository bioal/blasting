# HOP

## Dependencies
Requires Python3
- `python3` should be in the command path.

[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) should be installed.
- `blastp` should be in the command path.

## Usage


## Example
    $ 1.download_gene_files.py -l species_list.tsv -o genome
    $ 2.make_database.py -l gene_files.txt -o database
    $ 3.blast_search.py -n 4 -l databases.txt -o blast
    $ 4.make_matrix.py -i blast -l databases.txt -o matrix
