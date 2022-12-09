#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM REFSEQ_IDS_FILE BLAST_OUT
";

my %OPT;
getopts('', \%OPT);

if (!@ARGV) {
    print STDERR $USAGE;
    exit 1;
}

my ($REFSEQ_IDS_FILE, $BLAST_OUT) = @ARGV;
open(REFSEQ_IDS_FILE, "$REFSEQ_IDS_FILE") || die "$!";
my @SYMBOL = ();
my @REFSEQ = ();
while (<REFSEQ_IDS_FILE>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 5) {
        die;
    }
    push @SYMBOL, $f[2];
    push @REFSEQ, $f[4];
}
close(REFSEQ_IDS_FILE);

for (my $i=0; $i<@SYMBOL; $i++) {
    my $pattern = $REFSEQ[$i];
    $pattern =~ s/,/|/g;
    system "grep -E '$pattern' $BLAST_OUT > $SYMBOL[$i].out &";
}
