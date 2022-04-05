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

my %QUERY2SUBJ = ();
my %QUERY2SCORE = ();
my $PREV_QUERY = "";

!@ARGV && -t and die $USAGE;
while (<>) {
    chomp;
    if (/^#/) {
        next;
    }
    my @f = split("\t", $_);
    if (@f != 12) {
        die $_;
    }
    my $QUERY = $f[0];
    my $subject = $f[1];
    my $identify = $f[2];
    my $alignment_length = $f[3];
    my $mismatches = $f[4];
    my $gap_opens = $f[5];
    my $q_start = $f[6];
    my $q_end = $f[7];
    my $s_start = $f[8];
    my $s_end = $f[9];
    my $evalue = $f[10];
    my $bit_score = $f[11];
    eval_score($QUERY, $subject, $bit_score);
    $PREV_QUERY = $QUERY;
}
output_summary();

################################################################################
### Function ###################################################################
################################################################################
sub eval_score {
    my ($query, $subject, $bit_score) = @_;

    if ($query ne $PREV_QUERY) {
        output_summary();
        $QUERY2SCORE{$query} = $bit_score;
        $QUERY2SUBJ{$query} = $subject;
    } elsif ($bit_score > $QUERY2SCORE{$query}) {
        $QUERY2SCORE{$query} = $bit_score;
        $QUERY2SUBJ{$query} = $subject;
    }
}

sub output_summary {
    if ($PREV_QUERY) {
        print "$PREV_QUERY $QUERY2SUBJ{$PREV_QUERY} $QUERY2SCORE{$PREV_QUERY}\n";
    }
}
