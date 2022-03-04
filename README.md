# BLASTing

## Dependencies
Python3 should be installed.
- `python3` command is necessary (preferably in the command path).

[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) should be installed.
- `blastp` command is necessary (preferably in the command path).
- `install_blast.sh` will install `lib/blast/bin/blastp`

## Usage
### Using NCBI genomes
    1_download_genomes.py [-o OUT_DIR] SPECIES_LIST

    2_process_genomes.py [-p path/to/makeblastdb] GENOME_LIST

### In the case of UniProt proteomes
    1_download_proteomes.py [-o OUT_DIR] SPECIES_LIST
    
    2_process_proteomes.py [-p path/to/makeblastdb] PROTEOME_LIST

### Run BLAST
#### All against all
```
3_blast_all_vs_all.py -n CPU_CORES [-p path/to/blastp] [-o OUT_DIR] GENOME_LIST
```

#### For specific pairs
    3_blast_pair.py -n CPU_CORES [-p path/to/blastp] [-o OUT_DIR] GENOME_LIST

    4_make_matrix.py -i INPUT_DIR -o OUT_DIR GENOME_LIST

## Examples
### Using NCBI genomes
    mkdir work
    cd work

    1_download_genomes.py species_list.tsv
    # This will create data/genome/*, data/genome_list.tsv

    # This assumes makeblastdb is in the command path. Or, use -p option.
    2_process_genomes.py genome_list.tsv
    # This will create data/genes/*, data/db/*

    # This assumes blastp is in the command path. Or, use -p option.
    3_blast_pairs.py -n 40 genome_list.tsv
    # This will create data/blast/*, data/blast_log/*, data/blast_err/*

    4_make_matrix.py -i blast -o matrix genome_list.tsv
    # This will create data/matrix/*

### In the case of UniProt proteomes

    1_download_proteome.py species_list.tsv
    # This will create data/proteome/*, data/proteome_list.tsv

    # This assumes makeblastdb is in the command path. Or, use -p option.
    2_process_proteome.py proteome_list.tsv
    # This will create data/proteins/*, data/proteome_db/*
