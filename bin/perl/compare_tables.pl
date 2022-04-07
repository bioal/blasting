#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM FILE1 FIEL2
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 2) {
    print STDERR $USAGE;
    exit 1;
}
my ($FILE1, $FILE2) = @ARGV;

my %PAIR = ();

my $COUNT1 = 0;
open(FILE1, "$FILE1") || die "$!";
while (<FILE1>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 2) {
        die;
    }
    my $id1 = $f[0];
    my $id2 = $f[1];
    $id1 =~ s/\..*//;
    $id2 =~ s/\..*//;
    if ($PAIR{$id1}{$id2}) {
        die;
    }
    $PAIR{$id1}{$id2} = 1;
    $COUNT1 ++;
}
close(FILE1);

my $COUNT2 = 0;
my $COUNT_COMMON = 0;
open(FILE2, "$FILE2") || die "$!";
while (<FILE2>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 2) {
        die;
    }
    my $id1 = $f[0];
    my $id2 = $f[1];
    $id1 =~ s/\..*//;
    $id2 =~ s/\..*//;
    if ($PAIR{$id1}{$id2}) {
        $COUNT_COMMON ++;
    }
    $COUNT2 ++;
}
close(FILE2);

print $COUNT1 - $COUNT_COMMON, "\t";
print $COUNT_COMMON, "\t";
print $COUNT2 - $COUNT_COMMON, "\n";
