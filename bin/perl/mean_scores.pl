#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM
";

my %OPT;
getopts('v', \%OPT);

my %SCORE = ();
my %SCORES = ();
my %ORGANISM = ();
my %DESCR = ();
while (<>) {
    chomp;
    my @f = split(/\t/, $_);
    my $score = $f[11];
    my $descr = $f[14];
    if (/^1-1.out:(\S+)\s+(\S+)/) {
        my ($query, $target) = ($1, $2);
        save_score($query, $target, $score);
        $ORGANISM{$query} = 1;
        $ORGANISM{$target} = 1;
    } elsif (/^1-(\d+).out:(\S+)\s+(\S+)/) {
        my ($organism, $query, $target) = ($1, $2, $3);
        save_score($query, $target, $score);
        $ORGANISM{$query} = 1;
        $ORGANISM{$target} = $organism;
        $DESCR{$target} = $descr;
    } elsif (/^(\d+)-1.out:(\S+)\s+(\S+)/) {
        my ($organism, $query, $target) = ($1, $2, $3);
        save_score($query, $target, $score);
        $ORGANISM{$query} = $organism;
        $ORGANISM{$target} = 1;
    }    
}

for my $seq1 (keys %SCORE) {
    for my $seq2 (keys %{$SCORE{$seq1}}) {
        save_score_in_array($seq1, $seq2, $SCORE{$seq1}{$seq2});
    }
}

for my $seq1 (keys %SCORES) {
    for my $seq2 (keys %{$SCORES{$seq1}}) {
        my $org1 = $ORGANISM{$seq1};
        my $org2 = $ORGANISM{$seq2};
        my $descr = "";
        if ($org1 == 1 && $org2 == 1) {
            print "$org2\t";
            if ($OPT{v}) {
                print "$seq1\t$seq2\t";
            }
        } elsif ($org1 == 1) {
            print "$org2\t";
            if ($DESCR{$seq2}) {
                $descr = $DESCR{$seq2};
            }
            if ($OPT{v}) {
                print "$seq1\t$seq2\t";
            }
        } elsif ($org2 == 1) {
            print "$org1\t";
            if ($DESCR{$seq1}) {
                $descr = $DESCR{$seq1};
            }
            if ($OPT{v}) {
                print "$seq2\t$seq1\t";
            }
        } else {
            die "$org1 $org2";
        }

        print_scores($seq1, $seq2, @{$SCORES{$seq1}{$seq2}});

        if ($OPT{v}) {
            print "\t", $descr;
        }
        print "\n";
    }
}

################################################################################
### Function ###################################################################
################################################################################

sub print_scores {
    my ($seq1, $seq2, @score) = @_;
    
    if ($OPT{v}) {
        print "@score\t";
    }
    if (@score == 1) {
        print $score[0];
    } elsif (@score == 2) {
        print(($score[0] + $score[1]) / 2);
    } else {
        die;
    }
}

sub save_score {
    my ($seq1, $seq2, $score) = @_;

    ### Sum score for multi hits ###
    
    # if ($SCORE{$seq1}{$seq2}) {
    #     $SCORE{$seq1}{$seq2} += $score;
    # } else {
    #     $SCORE{$seq1}{$seq2} = $score;
    # }

    ### Max score for multi hits ###

    if ($SCORE{$seq1}{$seq2}) {
        if ($score > $SCORE{$seq1}{$seq2}) {
            print STDERR "$score\n";
            $SCORE{$seq1}{$seq2} = $score;
        }
    } else {
        $SCORE{$seq1}{$seq2} = $score;
    }

}


sub save_score_in_array {
    my ($seq1, $seq2, $score) = @_;
    
    if ($seq1 lt $seq2) {
        save_score_in_array_sub($seq1, $seq2, $score);
    } else {
        save_score_in_array_sub($seq2, $seq1, $score);
    }
}

sub save_score_in_array_sub {
    my ($seq1, $seq2, $score) = @_;
    
    if ($SCORES{$seq1}{$seq2}) {
        push @{$SCORES{$seq1}{$seq2}}, $score;
    } else {
        $SCORES{$seq1}{$seq2} = [$score];
    }
}
