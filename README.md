# HOP

## Dependencies
Python3 should be installed.
- `python3` command is necessary (preferably in the command path).

[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) should be installed.
- `blastp` command is necessary (preferably in the command path).

## Usage
    0_get_species_list.py [-o OUT_FILE]

    1_download_genomes.py [-o OUT_DIR] SPECIES_LIST

    2_process_genomes.py [-p path/to/makeblastdb] GENOME_LIST

    3_blast_search.py -n THREADS [-p path/to/blastp] [-o OUT_DIR] DB_LIST

    4_make_matrix.py -i INPUT_DIR -o OUT_DIR -l LIST

## Example
    cd ~/work/orthology/data

    ~/github/hop/src/0_get_species_list.py -o species_list.tsv
    # This is not mandatory.
    # This will create ./species_list.tsv (which is same as ~/github/hop/species_list.tsv)

    ~/github/hop/src/1_download_genomes.py ~/github/hop/species_list.tsv
    # This will create ~/work/orthology/data/genomes/*
    # and ~/work/orthology/data/genome_list.tsv

    ~/github/hop/src/2_process_genomes.py genome_list.tsv
    # makeblastdb command should be in the command path. Or, use -p option to specify the location
    # This will create ~/work/orthology/data/db/*
    # and ~/work/orthology/data/dbs.tsv

    ~/github/hop/src/3_blast_search.py -n 4 dbs.tsv
    # blastp command should be in the command path. Or, use -p option to specify the location
    # This will create ~/work/orthology/data/blast/*

    ~/github/hop/src/4_make_matrix.py -i data/genome/blast -o data/matrix -l databases.txt
    # This will create ~/work/orthology/data/matrix/*
