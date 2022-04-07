#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: cat TABLE | $PROGRAM SPECIES_LIST
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 1) {
    print STDERR $USAGE;
    exit 1;
}
my ($LIST_FILE) = @ARGV;

my %TAXID = ();
open(LIST, "$LIST_FILE") || die "$!";
while (<LIST>) {
    chomp;
    my ($id, $taxid) = split("\t", $_);
    if ($taxid =~ /^\d+$/) {
        $TAXID{$taxid} = 1;
    }
    
}
close(LIST);

while (<STDIN>) {
    my @f = split(/\t/, $_);
    my $taxid = $f[0];
    if ($TAXID{$taxid}) {
        print;
    }
}
