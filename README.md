# HOP

## Dependencies
Requires Python3
- `python3` should be in the command path.

[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) should be installed.
- `blastp` should be in the command path.

## Usage
    1_download_gene_files.py -l [list_file] -o [output_folder]
    2_make_database.py -l [list_file] -o [output_folder] -p [makeblastdb command (optional)]
    3_blast_search.py -l [list_file] -o [output_folder] -n [number of threads] -p [makeblastdb command (optional)]
    4_make_matrix.py -l [list_file] -i [input_folder] -o [output_folder]


## Example
    cd ~/work/orthology/data
    
    ~/github/hop/src/1_download_gene_files.py -l ~/github/hop/species_list.tsv -o data/genome
    # ~/work/orthology/data/genome/* will be generated.
    
    ~/github/hop/src/2_make_database.py -l gene_files.txt -o data/genome/database
    # ~/work/orthology/data/genome/database/* will be generated.
    
    ~/github/hop/src/3_blast_search.py -l databases.txt -n 4 -o data/genome/blast
    # ~/work/orthology/data/blast/* will be generated.
    
    ~/github/hop/src/4_make_matrix.py -l databases.txt -i data/genome/blast -o data/matrix
    # ~/work/orthology/data/matrix/* will be generated.
