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
my $COUNT;
my $PREV_QUERY;
my $PREV_TARGET;
while (<>) {
    chomp;
    if (/^# (\d+) hits found/) {
        check_count();
        $HITS = $1;
        $COUNT = 0;
    } elsif (/^#/) {
    } else {
        $COUNT++;
        my @f = split(/\t/, $_);
        if (@f != 12) {
            die $_;
        }
        my $query = $f[0];
        my $target = $f[1];
        if ($COUNT == 1) {
            # print $query, "\t", $target, "\n";
            print $_, "\n";
            $PREV_QUERY = $query;
            $PREV_TARGET = $target;
        } else {
            if (same_query_and_target($query, $target)) {
                print $_, "\n";
            }
        }
    }
}
check_count();

################################################################################
### Functions ##################################################################
################################################################################

sub same_query_and_target {
    my ($query, $target) = @_;

    if (defined($PREV_QUERY) && defined($PREV_TARGET)) {
        if ($query eq $PREV_QUERY && $target eq $PREV_TARGET) {
            return 1;
        }
    }
}

sub check_count {
    if (defined($HITS) && defined($COUNT)) {
        if ($HITS == $COUNT) {
        } else {
            die;
        }
    }
}
