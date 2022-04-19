#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM HIT THRESHOLD
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 2) {
    print STDERR $USAGE;
    exit 1;
}
my ($HIT, $THRESHOLD) = @ARGV;

my %THRESHOLD = ();
open(THRESHOLD, "$THRESHOLD") || die "$!";
while (<THRESHOLD>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 2) {
        die;
    }
    my ($query, $score) = @f;
    $THRESHOLD{$query} = $score;
}
close(THRESHOLD);

open(HIT, "$HIT") || die "$!";
while (<HIT>) {
    chomp;
    my @f = split(/\t/, $_);
    my $query = $f[0];
    my $target = $f[1];
    my $score = $f[11];
    if ($THRESHOLD{$query}) {
        if ($score > $THRESHOLD{$query}) {
            print "$query\t$target\t$score > $THRESHOLD{$query}\n";
        } elsif ($score == $THRESHOLD{$query}) {
            print "$query\t$target\t$score = $THRESHOLD{$query}\n";
        # } elsif ($score >= 0.99 * $THRESHOLD{$query}) {
        #     print "$query\t$target\t$score >= 0.99 $THRESHOLD{$query}\n";
        }
    } else {
        print "$query\t$target\t$score without threshold\n";
    }
}
close(HIT);
