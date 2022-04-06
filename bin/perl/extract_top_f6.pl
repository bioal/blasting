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
my $HITS;
my $PREV_QUERY;
my $PREV_TARGET;
while (<>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 12) {
        die $_;
    }
    my $query = $f[0];
    my $target = $f[1];
    if (is_new_query($query)) {
        print $_, "\n";
        $PREV_QUERY = $query;
        $PREV_TARGET = $target;
    } else {
        if (same_query_and_target($query, $target)) {
            print $_, "\n";
        }
    }
}

################################################################################
### Functions ##################################################################
################################################################################
sub is_new_query {
    my ($query) = @_;
    
    if (!defined($PREV_QUERY)) {
        return 1;
    } elsif ($PREV_QUERY ne $query) {
        return 1;
    }
}

sub same_query_and_target {
    my ($query, $target) = @_;

    if (defined($PREV_QUERY) && defined($PREV_TARGET)) {
        if ($query eq $PREV_QUERY && $target eq $PREV_TARGET) {
            return 1;
        }
    }
}
