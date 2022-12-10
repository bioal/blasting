#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM SYMBOL.out blast.out
-v: verbose
-t top_score_to_human
";

my %OPT;
getopts('vt:', \%OPT);

my %TOP = ();
my %TOP_SCORE = ();
if ($OPT{t}) {
    open(TOP, "$OPT{t}") || die "$!";
    while (<TOP>) {
        chomp;
        my @f = split(/\t/, $_);
        my $query = $f[0];
        my $hit = $f[1];
        my $score = $f[2];
        $TOP{$query}{$hit} = 1;
        $TOP_SCORE{$query} = $score;
    }
    close(TOP);
}

if (!@ARGV) {
    print STDERR $USAGE;
    exit 1;
}
my ($FILE, $ALL) = @ARGV;
my $SYMBOL = $FILE;
$SYMBOL =~ s/\.out$//;

my %SEED = ();
open(REF, "/home/chiba/github/bioal/blasting/examples/13_genes.refseq.tsv") || die "$!";
while (<REF>) {
    chomp;
    my @f = split(/\t/, $_);
    my $symbol = $f[2];
    if ($symbol eq $SYMBOL) {
        my $refseq_ids = $f[4];
        my @refseq_id = split(",", $refseq_ids);
        for my $refseq_id (@refseq_id) {
            $SEED{$refseq_id} = 1;
        }
    }
}
close(REF);

my %DESCR = ();
if ($ALL) {
    open(ALL, "$ALL") || die "$!";
    while (<ALL>) {
        chomp;
        my @f = split(/\t/, $_);
        my $descr = $f[14];
        if (/^1-1.out:(\S+)\s+(\S+)/) {
        } elsif (/^1-(\d+).out:(\S+)\s+(\S+)/) {
            my ($organism, $query, $target) = ($1, $2, $3);
            $DESCR{$target} = $descr;
        }
    }
    close(ALL);
}

my %SCORE = ();
my %SCORES = ();
my %ORGANISM = ();
open(FILE, "$FILE") || die "$!";
while (<FILE>) {
    chomp;
    my @f = split(/\t/, $_);
    my $score = $f[11];
    my $descr = $f[14];
    if (/^1-1.out:(\S+)\s+(\S+)/) {
        my ($query, $target) = ($1, $2);
        save_score($query, $target, $score);
        $ORGANISM{$query} = 1;
        $ORGANISM{$target} = 1;
        if (!$SEED{$query}) {
            $DESCR{$query} = $descr;
        }
        if (!$SEED{$target}) {
            $DESCR{$target} = $descr;
        }
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
close(FILE);

for my $seq1 (keys %SCORE) {
    for my $seq2 (keys %{$SCORE{$seq1}}) {
        save_score_in_array($seq1, $seq2, $SCORE{$seq1}{$seq2});
    }
}

if ($OPT{v}) {
    open(PIPE, "|sort -t '\t' -k5,5nr -k1,1n") || die "$!";
} else {
    open(PIPE, "|sort -t '\t' -k2,2nr -k1,1n") || die "$!";
}
for my $seq1 (keys %SCORES) {
    for my $seq2 (keys %{$SCORES{$seq1}}) {
        my $org1 = $ORGANISM{$seq1};
        my $org2 = $ORGANISM{$seq2};
        my @top_hit;
        my $top_score = "";
        my $bbh = 0;
        if ($org1 == 1 && $org2 == 1) {
            print PIPE "$org2\t";
            if ($SEED{$seq1} && $SEED{$seq2}) {
                $bbh = 1;
            }
            if ($OPT{v}) {
                print PIPE "$seq1\t$seq2\t";
            }
        } elsif ($org1 == 1) {
            print PIPE "$org2\t";
            @top_hit = keys %{$TOP{$seq2}};
            if ($TOP_SCORE{$seq2}) {
                $top_score = $TOP_SCORE{$seq2};
            } else {
                print STDERR "no top hit for $org2 $seq2\n";
            }
            if ($OPT{v}) {
                print PIPE "$seq1\t$seq2\t";
            }
        } elsif ($org2 == 1) {
            print PIPE "$org1\t";
            @top_hit = keys %{$TOP{$seq1}};
            if ($TOP_SCORE{$seq1}) {
                $top_score = $TOP_SCORE{$seq1};
            } else {
                print STDERR "no top hit for $org1 $seq1\n";
            }
            if ($OPT{v}) {
                print PIPE "$seq2\t$seq1\t";
            }
        } else {
            die "$org1 $org2";
        }

        my $mean_score = print_scores(@{$SCORES{$seq1}{$seq2}});

        for my $hit (@top_hit) {
            if ($SEED{$hit}) {
                $bbh = 1;
            }
        }

        if ($OPT{v}) {
            my $descr = "";
            if ($DESCR{$seq1} && $DESCR{$seq2}) {
                die;
            }
            if ($DESCR{$seq1}) {
                $descr = $DESCR{$seq1};
            }
            if ($DESCR{$seq2}) {
                $descr = $DESCR{$seq2};
            }
            print PIPE "\t", $descr;
        }

        my $ratio = "";
        if ($top_score) {
            $ratio = sprintf("%.3f", $mean_score / $top_score);
        }
        print PIPE "\t$bbh";
        if ($OPT{v}) {
            print PIPE "\t$top_score";
            print PIPE "\t$ratio";
            print PIPE "\t@top_hit";
        }
        print PIPE "\n";
    }
}
close(PIPE);

################################################################################
### Function ###################################################################
################################################################################

sub print_scores {
    my (@score) = @_;
    
    if ($OPT{v}) {
        print PIPE "@score\t";
    }
    if (@score == 1) {
        print PIPE $score[0];
        return $score[0]
    } elsif (@score == 2) {
        print PIPE ($score[0] + $score[1]) / 2;
        return(($score[0] + $score[1]) / 2);
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
