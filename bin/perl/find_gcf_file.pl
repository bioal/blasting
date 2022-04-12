#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM ORGANISM_LIST ASSEMBLY_REPORTS
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 2) {
    print STDERR $USAGE;
    exit 1;
}
my ($LIST_FILE, $ASSEMBLY_REPORTS) = @ARGV;

my %ID = ();
open(LIST, "$LIST_FILE") || die "$!";
while (<LIST>) {
    chomp;
    my ($id, $taxid) = split("\t", $_);
    if ($id =~ /^\d+$/) {
        $ID{$taxid} = $id;
    }
}
close(LIST);

open(ASSEMBLY_REPORTS, "$ASSEMBLY_REPORTS") || die "$!";
while (<>) {
    chomp;
    if (/^#/) {
        next;
    }
    my @f = split(/\t/, $_);
    if (@f >= 7) {
        my $category = $f[4];
        my $taxid = $f[5];
        my $species_taxid = $f[6];
        if ($category eq "na") {
            next;
        }
        if ($ID{$taxid}) {
            print $ID{$taxid}, "\t", $_, "\n";
        } elsif ($ID{$species_taxid}) {
            print $ID{$species_taxid}, "\t", $_, "\n";
        }
    }
}
close(ASSEMBLY_REPORTS);
