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
my $TOP_SCORE;
while (<>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f < 12) {
        die;
    }
    my $query = $f[0];
    my $hit = $f[1];
    my $score = $f[11];
    if (! $CURRENT_QUERY or $query ne $CURRENT_QUERY) {
        print $query, "\t", $hit, "\n";
        $TOP_SCORE = $score;
    } elsif ($query eq $CURRENT_QUERY and $score eq $TOP_SCORE) {
        print $query, "\t", $hit, "\n";
    }
    $CURRENT_QUERY = $query;
}
