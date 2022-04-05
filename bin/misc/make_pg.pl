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
while (<>) {
    if (/^#/) {
    } else {
        my @f = split(/\t/, $_);
        if (@f != 12) {
            die $_;
        }
        my $query = $f[0];
        my $subject = $f[1];
        my $identity = $f[2];
        my $alignment_length = $f[3];
        my $mismatches = $f[4];
        my $gap_opens = $f[5];
        my $q_start = $f[6];
        my $q_end = $f[7];
        my $s_start = $f[8];
        my $s_end = $f[9];
        my $evalue = $f[10];
        my $bit_score = $f[11];
        print "$query -> $subject";
        print " identity: $identity";
        print "\n";
    }
}
