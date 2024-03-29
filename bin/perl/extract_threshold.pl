#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM ID
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 1) {
    print STDERR $USAGE;
    exit 1;
}
my ($ID) = @ARGV;

my %THRESHOLD = ();

for (my $i=1; $i<=21; $i++) {
    if ($i ne $ID) {
        open_file("${ID}-${i}.out.top_score");
    }
}

for my $key (keys(%THRESHOLD)) {
    print $key, "\t", $THRESHOLD{$key}, "\n";
}

################################################################################
### Function ###################################################################
################################################################################

sub open_file {
    my ($file) = @_;
    
    open(FILE, "$file") || die "$!";
    while (<FILE>) {
        chomp;
        my @f = split(/\t/, $_);
        if (@f != 3) {
            die;
        }    
        my ($query, $target, $score) = @f;
        if ($THRESHOLD{$query}) {
            if ($score > $THRESHOLD{$query}) {
                $THRESHOLD{$query} = $score;
            }
        } else {
            $THRESHOLD{$query} = $score;
        }
    }
    close(FILE);
}
