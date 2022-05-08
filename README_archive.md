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

### Summarize results
    cd blast.out
    ../bin/4_extract_top_score.py *out -n 90
    for i in {1..21}; do ../bin/perl/extract_threshold.pl $i > $i.threshold; done &
    for i in {1..21}; do ../bin/perl/extract_paralogs.pl $i-$i.out $i.threshold > $i-$i.paralog_score & done
    for i in {1..21}; do c $i-$i.paralog_score l ../bin/perl/summarize_paralog.pl > $i.paralogs & done
    cd ..
    5_extract_bbh_org.py input/genomes_downloaded.tsv -i blast.out -o blast.out -n 50
    cd blast.out
    ../bin/6_make_matrix.pl ../homologene_species.tsv ../input/gene_refseq.human > ../blast.out.mat &

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