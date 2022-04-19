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

my %HIT = ();
while (<>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 3) {
        die;
    }
    my $query = $f[0];
    my $target = $f[1];
    if ($query ne $target) {
        $HIT{$query}{$target} = 1;
    }
}

for my $key (sort keys(%HIT)) {
    # if ($HIT{$key}{$key}) {
    # } else {
    #     die $key;
    # }
    my @targets = sort keys(%{$HIT{$key}});
    if (@targets == 1 && $targets[0] eq $key) {
        # print "$key @targets same\n";
    } else {
        print "$key\t", join(",", @targets), "\n";
    }
}
