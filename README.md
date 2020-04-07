# HOP

## Dependencies
Requires Python3
- `python3` should be in the command path.

[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) should be installed.
- `blastp` should be in the command path.

## Usage
    1_download_gene_files.py -l LIST -o OUTPUT_DIR

    2_make_database.py -l LIST -o OUTPUT_DIR [-p path/to/makeblastdb]

    3_blast_search.py -l LIST -o OUTPUT_DIR -n THREADS [-p path/to/blastp]

    4_make_matrix.py -l LIST -i INPUT_DIR -o OUTPUT_DIR

## Example
    $ cd ~/work/orthology/data
    
    $ ~/github/hop/src/1_download_gene_files.py -l ~/github/hop/species_list.tsv -o data/genome
~/work/orthology/data/genome/* will be generated.
    
    $ ~/github/hop/src/2_make_database.py -l gene_files.txt -o data/genome/database
~/work/orthology/data/genome/database/* will be generated.
    
    $ ~/github/hop/src/3_blast_search.py -l databases.txt -n 4 -o data/genome/blast
~/work/orthology/data/blast/* will be generated.
    
    $ ~/github/hop/src/4_make_matrix.py -l databases.txt -i data/genome/blast -o data/matrix
~/work/orthology/data/matrix/* will be generated.
