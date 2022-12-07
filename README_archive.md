## Usage
### In the case of UniProt proteomes
    1_download_proteomes.py [-o OUT_DIR] SPECIES_LIST
    
    2_process_proteomes.py [-p path/to/makeblastdb] PROTEOME_LIST

### Run BLAST
#### For specific pairs
    3_blast_pair.py -n CPU_CORES [-p path/to/blastp] [-o OUT_DIR] GENOME_LIST

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
