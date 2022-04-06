#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM
";

my %OPT;
getopts('', \%OPT);

!@ARGV && -t and die $USAGE;
my $CURRENT_QUERY;
while (<>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f < 12) {
        die;
    }
    my $query = $f[0];
    my $hit = $f[1];
    if (! $CURRENT_QUERY or $query ne $CURRENT_QUERY) {
        print $query, "\t", $hit, "\n";
    }
    $CURRENT_QUERY = $query;
}
