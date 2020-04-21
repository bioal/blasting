# HOP

## Dependencies
Python3 should be installed.
- `python3` command is necessary (preferably in the command path).

[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) should be installed.
- `blastp` command is necessary (preferably in the command path).

## Usage
    0_get_species_list.py [-o OUT_FILE]

    1_download_genomes.py [-o OUT_DIR] SPECIES_LIST
    1_download_proteomes.py [-o OUT_DIR] SPECIES_LIST

    2_process_genomes.py [-p path/to/makeblastdb] GENOME_LIST
    2_process_proteomes.py [-p path/to/makeblastdb] PROTEOME_LIST

    3_blast_search.py -n CPU_CORES [-p path/to/blastp] [-o OUT_DIR] GENOME_LIST

    4_make_matrix.py -i INPUT_DIR -o OUT_DIR GENOME_LIST

## Example
    cd ~/work/orthology/data

    ~/github/hop/src/0_get_species_list.py -o species_list.tsv
    # This is not mandatory.
    # This will create ./species_list.tsv (which is same as ~/github/hop/species_list.tsv)

    ~/github/hop/src/1_download_genomes.py ~/github/hop/species_list.tsv
    # This will create ~/work/orthology/data/genome/*
    # and ~/work/orthology/data/genome_list.tsv

    ~/github/hop/src/2_process_genomes.py genome_list.tsv
    # This assumes makeblastdb is in the command path. Or, use -p option.
    # This will create ~/work/orthology/data/genes/*
    # and ~/work/orthology/data/db/*

    ~/github/hop/src/3_blast_search.py -n 40 genome_list.tsv
    # This assumes blastp is in the command path. Or, use -p option.
    # This will create ~/work/orthology/data/blast/*
    # This will create ~/work/orthology/data/blast_log/*
    # This will create ~/work/orthology/data/blast_err/*

    ~/github/hop/src/4_make_matrix.py -i blast -o matrix genome_list.tsv
    # This will create ~/work/orthology/data/matrix/*
