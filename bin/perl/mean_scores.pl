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

my %SCORE_SUM = ();
my %SCORE = ();
my %ORGANISM = ();
while (<>) {
    chomp;
    my @f = split(/\t/, $_);
    my $score = $f[11];
    if (/^1-1.out:(\S+)\s+(\S+)/) {
        my ($query, $target) = ($1, $2);
        # print "1\t$query\t$target\tself\t", $score, "\n";
        score_sum($query, $target, $score);
        $ORGANISM{$query} = 1;
        $ORGANISM{$target} = 1;
    } elsif (/^1-(\d+).out:(\S+)\s+(\S+)/) {
        my ($organism, $query, $target) = ($1, $2, $3);
        # print $organism, "\t$query\t$target\tforward\t", $score, "\n";
        score_sum($query, $target, $score);
        $ORGANISM{$query} = 1;
        $ORGANISM{$target} = $organism;
    } elsif (/^(\d+)-1.out:(\S+)\s+(\S+)/) {
        my ($organism, $query, $target) = ($1, $2, $3);
        # print $organism, "\t$target\t$query\treverse\t", $score, "\n";
        score_sum($query, $target, $score);
        $ORGANISM{$query} = $organism;
        $ORGANISM{$target} = 1;
    }    
}

for my $seq1 (keys %SCORE_SUM) {
    for my $seq2 (keys %{$SCORE_SUM{$seq1}}) {
        # print "$seq1\t$seq2\t";
        # print $SCORE_SUM{$seq1}{$seq2};
        # print "\n";
        save_score($seq1, $seq2, $SCORE_SUM{$seq1}{$seq2});
    }
}

for my $seq1 (keys %SCORE) {
    for my $seq2 (keys %{$SCORE{$seq1}}) {
        print_scores($seq1, $seq2, @{$SCORE{$seq1}{$seq2}});
    }
}

################################################################################
### Function ###################################################################
################################################################################

sub print_scores {
    my ($seq1, $seq2, @score) = @_;
    
    my $n_score = @score;
    my $org1 = $ORGANISM{$seq1};
    my $org2 = $ORGANISM{$seq2};
    my $org = 0;
    if ($org1 == 1 && $org2 == 1) {
        $org = 1;
    } elsif ($org1 == 1) {
        $org = $org2;
    } elsif ($org2 == 1) {
        $org = $org1;
    } else {
        die "$org1 $org2";
    }

    print $org, "\t";
    if ($OPT{v}) {
        print_seq_ids($org1, $org2, $seq1, $seq2);
        print "\t@score\t";
        print "$n_score\t";
    }
    if ($n_score == 1) {
        print $score[0];
    } elsif ($n_score == 2) {
        print(($score[0] + $score[1]) / 2);
    } else {
        die;
    }
    print "\n";
}

sub print_seq_ids {
    my ($org1, $org2, $seq1, $seq2) = @_;
    
    print "$org1\t$org2\t$seq1\t$seq2";
}

sub score_sum {
    my ($seq1, $seq2, $score) = @_;

    # if ($SCORE_SUM{$seq1}{$seq2}) {
    #     $SCORE_SUM{$seq1}{$seq2} += $score;
    # } else {
    #     $SCORE_SUM{$seq1}{$seq2} = $score;
    # }

    if ($SCORE_SUM{$seq1}{$seq2}) {
        if ($score > $SCORE_SUM{$seq1}{$seq2}) {
            print STDERR "$score\n";
            $SCORE_SUM{$seq1}{$seq2} = $score;
        }
    } else {
        $SCORE_SUM{$seq1}{$seq2} = $score;
    }
}


sub save_score {
    my ($seq1, $seq2, $score) = @_;
    
    if ($seq1 lt $seq2) {
        save_score_sub($seq1, $seq2, $score);
    } else {
        save_score_sub($seq2, $seq1, $score);
    }
}

sub save_score_sub {
    my ($seq1, $seq2, $score) = @_;
    
    if ($SCORE{$seq1}{$seq2}) {
        push @{$SCORE{$seq1}{$seq2}}, $score;
    } else {
        $SCORE{$seq1}{$seq2} = [$score];
    }
}
