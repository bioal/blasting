#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM SPECIES_LIST GENE_REFSEQ
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 2) {
    print STDERR $USAGE;
    exit 1;
}
my ($SPECIES_LIST, $GENE_REFSEQ) = @ARGV;

my @SPECIES = ();
open(SPECIES_LIST, "$SPECIES_LIST") || die "$!";
while (<SPECIES_LIST>) {
    chomp;
    my ($id, $taxid) = split("\t", $_);
    if ($id =~ /^\d+$/) {
        push @SPECIES, $id;
    }    
}
close(SPECIES_LIST);

my %GET_GENE_ID = ();
open(GENE_REFSEQ, "$GENE_REFSEQ") || die "$!";
while (<GENE_REFSEQ>) {
    chomp;
    my @f = split(/\t/, $_);
    my $geneid = $f[0];
    my $refseq_id = $f[1];
    $refseq_id =~ s/\.\d+//;
    $GET_GENE_ID{$refseq_id} = $geneid;
}
close(GENE_REFSEQ);

my %ORTH = ();
for (my $i=1; $i<@SPECIES; $i++) {
    read_bbh($SPECIES[$i], "$SPECIES[0]-$SPECIES[$i].bbh");
}

my @PROT = keys %ORTH;
for my $prot (sort @PROT) {
    print_matrix($prot);
}

################################################################################
### Function ###################################################################
################################################################################

sub get_gene_id {
    my ($refseq_id) = @_;

    my $geneid = "0";
    $refseq_id =~ s/\.\d+//;
    if ($GET_GENE_ID{$refseq_id}) {
        $geneid = $GET_GENE_ID{$refseq_id};
    }

    return $geneid;
}

sub print_matrix {
    my ($prot) = @_;

    print get_gene_id($prot);
    print "\t";
    print "$prot";
    for (my $i=1; $i<@SPECIES; $i++) {
        my @hit = keys %{$ORTH{$prot}{$SPECIES[$i]}};
        if (@hit) {
            print "\t", join(",", @hit);
        } else {
            print "\t0";
        }
    }
    print "\n";
}

sub read_bbh {
    my ($org, $file) = @_;

    open(FILE, "$file") || die "$!";
    while (<FILE>) {
        chomp;
        my @f = split(/\t/, $_);
        if (@f != 2) {
            die;
        }
        my ($prot1, $prot2) = @f;
        $ORTH{$prot1}{$org}{$prot2} = 1;
    }
    close(FILE);
}
