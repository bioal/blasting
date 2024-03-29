#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM
";

my %OPT;
getopts('d:', \%OPT);

if (!@ARGV) {
    print STDERR $USAGE;
    exit 1;
}
my ($GENE) = @ARGV;

my $SPECIES_TABLE = $OPT{d} || die $USAGE;
my @SEQ_FILE = ();
my %SEQ_REFSEQ = ();
read_species_table($SPECIES_TABLE);

my %REFSEQ = ();
my %SEQ = ();
STDOUT->autoflush;
while (<STDIN>) {
    chomp;
    my @f = split(/\t/, $_);
    my $gene = $f[0];
    if ($gene eq $GENE) {
        for (my $i=1; $i<@f; $i++) {
            if ($f[$i]) {
                save_refseq($f[$i], $i);
            }
        }
    }
}

for my $seq (keys %SEQ_REFSEQ) {
    extract_gene_seq($seq);
}

for (my $i=1; $i<=21; $i++) {
    if ($REFSEQ{$i}) {
        for my $refseq (keys %{$REFSEQ{$i}}) {
            # print STDERR "$i $refseq\n";
            print $SEQ{$refseq};
        }
    }
}


################################################################################
### Function ###################################################################
################################################################################

sub extract_gene_seq {
    my ($seq) = @_;

    open(SEQ, "$seq") || die "$!";
    my $reading = "";
    while (<SEQ>) {
        chomp;
        if (/^>(\S+)/) {
            my $id = $1;
            if ($SEQ_REFSEQ{$seq}{$id}) {
                $reading = $id;
            } else {
                $reading = "";
            }
        }
        if ($reading) {
            if ($SEQ{$reading}) {
                $SEQ{$reading} .= $_ . "\n";
            } else {
                $SEQ{$reading} = $_ . "\n";
            }
        }
    }
    close(SEQ);    
}

sub read_species_table {
    my ($species_table) = @_;
    open(SPECIES_TABLE, "$species_table") || die "$species_table: $!";
    while (<SPECIES_TABLE>) {
        chomp;
        my @f = split(/\t/, $_);
        if (@f != 2) {
            die;
        }
        my $species_id = $f[0];
        my $seq_file = $f[1];
        $SEQ_FILE[$species_id] = $seq_file;
    }
    close(SPECIES_TABLE);
}

sub save_refseq {
    my ($cell, $species_id) = @_;

    my $seq_file = $SEQ_FILE[$species_id];
    my @refseq = split(",", $cell);
    for my $refseq (@refseq) {
        $REFSEQ{$species_id}{$refseq} = 1;
        $SEQ_REFSEQ{$seq_file}{$refseq} = 1;
    }
}
