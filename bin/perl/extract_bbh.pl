#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM ID1 ID2
-i INPUT_DIR
";

my %OPT;
getopts('i:', \%OPT);
if (@ARGV != 2) {
    print STDERR $USAGE;
    exit 1;
}
my ($ID1, $ID2) = @ARGV;

my $DIR = "";
if (defined $OPT{i}) {
    $DIR = $OPT{i} . "/";
}

my %HIT = ();
open(FILE1, "${DIR}${ID1}-${ID2}.out.top_score") || die;
while (<FILE1>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 3) {
        die;
    }
    my $id1 = $f[0];
    my $id2 = $f[1];
    $HIT{$id1}{$id2} = 1;
}
close(FILE1);

open(FILE2, "${DIR}${ID2}-${ID1}.out.top_score") || die;
while (<FILE2>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 3) {
        die;
    }
    my $id2 = $f[0];
    my $id1 = $f[1];
    if ($HIT{$id1}{$id2}) {
        print "$id1\t$id2\n"
    } else {
        # print STDERR "WARNING: $id1 not found\n";
    }
}
close(FILE2);
