# BLASTing

## Dependencies

Python3 should be installed.
- `python3` command is necessary (preferably in the command path).

[BLAST+](https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) should be installed.
- `blastp` command is necessary (preferably in the command path).
- `install_blast.sh` will install `lib/blast/bin/blastp`

## Usage

### Data preparation

```
1_download_genomes.py [-o OUT_DIR] homologene_species.tsv
```

```
2_process_genomes.py [-p path/to/makeblastdb] data/genomes_downloaded.tsv
```

### Run BLAST

```
3_blast_all_vs_all.py [-p path/to/blastp] [-o OUT_DIR] -n 45 data/genomes_downloaded.tsv > blast.queue 2> blast.err &
```

### Summarize results

```
cd blast.out
4_extract_top_score.py *out -n 90
for i in {1..21}; do ../bin/perl/extract_threshold.pl $i > $i.threshold; done &
for i in {1..21}; do ../bin/perl/extract_paralogs.pl $i-$i.out $i.threshold > $i-$i.paralog_score & done
for i in {1..21}; do c $i-$i.paralog_score | ../bin/perl/summarize_paralog.pl > $i.paralogs & done
cd ..
```

```
5_extract_bbh_org.py input/genomes_downloaded.tsv -i blast.out -o blast.out -n 50
```

```
cd blast.out
6_make_matrix.pl ../homologene_species.tsv ../input/gene_refseq.human > ../blast.out.mat &
```
