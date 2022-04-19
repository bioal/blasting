#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM SPECIES_LIST
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 1) {
    print STDERR $USAGE;
    exit 1;
}
my ($LIST) = @ARGV;

my @SPECIES = ();
open(LIST, "$LIST") || die "$!";
while (<LIST>) {
    chomp;
    my ($id, $taxid) = split("\t", $_);
    if ($id =~ /^\d+$/) {
        push @SPECIES, $id;
    }    
}
close(LIST);

my %ORTH = ();
for (my $i=1; $i<@SPECIES; $i++) {
    read_bbh($SPECIES[$i], "$SPECIES[0]-$SPECIES[$i].bbh");
}

my @GENE = keys %ORTH;
for my $gene (sort @GENE) {
    print_matrix($gene);
}

################################################################################
### Function ###################################################################
################################################################################

sub print_matrix {
    my ($geneid) = @_;

    print "$geneid";
    for (my $i=1; $i<@SPECIES; $i++) {
        my @gene = keys %{$ORTH{$geneid}{$SPECIES[$i]}};
        if (@gene) {
            print "\t", join(",", @gene);
        } else {
            print "\t0";
        }
    }
    print "\n";
}

sub read_bbh {
    my ($id, $file) = @_;

    open(FILE, "$file") || die "$!";
    while (<FILE>) {
        chomp;
        my @f = split(/\t/, $_);
        if (@f != 2) {
            die;
        }
        my ($geneid1, $geneid2) = @f;
        $ORTH{$geneid1}{$id}{$geneid2} = 1;
    }
    close(FILE);
}
