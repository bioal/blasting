#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM ID1 ID2 GENE_REFSEQ
-i INPUT_DIR
";

my %OPT;
getopts('i:', \%OPT);
if (@ARGV != 3) {
    print STDERR $USAGE;
    exit 1;
}
my ($ID1, $ID2, $GENE_REFSEQ) = @ARGV;

my $DIR = "";
if (defined $OPT{i}) {
    $DIR = $OPT{i} . "/";
}

my %GET_VER = ();
my %REFSEQ_GENE = ();
my %REFSEQ_VER_GENE = ();
open(GENE_REFSEQ, "$GENE_REFSEQ") || die "$!";
while (<GENE_REFSEQ>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 2) {
        die;
    }
    my ($gene, $refseq_ver) = @f;
    my $refseq = $refseq_ver;
    $refseq =~ s/\..*//;
    $GET_VER{$refseq} = $refseq_ver;
    $REFSEQ_GENE{$refseq} = $gene;
    $REFSEQ_VER_GENE{$refseq_ver} = $gene;
}
close(GENE_REFSEQ);

my %HIT = ();
open(FILE1, "${DIR}${ID1}-${ID2}.out.top") || die;
while (<FILE1>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 2) {
        die;
    }
    my $id1 = $f[0];
    my $id2 = $f[1];
    my $geneid1 = refseq_gene($id1);
    my $geneid2 = refseq_gene($id2);
    if ($geneid1 and $geneid2) {
        $HIT{$geneid1}{$geneid2} = 1;
    }
}
close(FILE1);

open(FILE2, "${DIR}${ID2}-${ID1}.out.top") || die;
while (<FILE2>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 2) {
        die;
    }
    my $id2 = $f[0];
    my $id1 = $f[1];
    my $geneid2 = refseq_gene($id2);
    my $geneid1 = refseq_gene($id1);
    if ($geneid1 and $geneid2 and $HIT{$geneid1}{$geneid2}) {
        print "$geneid1\t$geneid2\n"
    }
}
close(FILE2);

################################################################################
### Functions ##################################################################
################################################################################

sub refseq_gene {
    my ($refseq_ver) = @_;

    if ($REFSEQ_VER_GENE{$refseq_ver}) {
        return $REFSEQ_VER_GENE{$refseq_ver};
    }

    print STDERR "refseq_gene cannot find $refseq_ver\t";

    my $refseq = $refseq_ver;
    $refseq =~ s/\..*//;
    if ($REFSEQ_GENE{$refseq}) {
        print STDERR "found ", $GET_VER{$refseq}, "\n";
        return $REFSEQ_GENE{$refseq};
    }

    print STDERR "skip $refseq_ver\n";
}
