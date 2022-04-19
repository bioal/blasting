#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM SPECIES_LIST
";

my %OPT;
getopts('', \%OPT);

if (@ARGV != 1) {
    print STDERR $USAGE;
    exit 1;
}
my ($SPECIES_LIST) = @ARGV;

my @SPECIES = ();
open(SPECIES_LIST, "$SPECIES_LIST") || die "$!";
while (<SPECIES_LIST>) {
    chomp;
    my ($id, $taxid) = split("\t", $_);
    if ($id =~ /^\d+$/) {
        push @SPECIES, $id;
    }    
}
close(SPECIES_LIST);

my %ORTH = ();
for (my $i=1; $i<@SPECIES; $i++) {
    read_bbh($SPECIES[$i], "$SPECIES[0]-$SPECIES[$i].bbh");
}

my @PROT = keys %ORTH;
for my $prot (sort @PROT) {
    print_matrix($prot);
}

################################################################################
### Function ###################################################################
################################################################################

sub print_matrix {
    my ($prot) = @_;

    print "$prot";
    for (my $i=1; $i<@SPECIES; $i++) {
        my @hit = keys %{$ORTH{$prot}{$SPECIES[$i]}};
        if (@hit) {
            print "\t", join(",", @hit);
        } else {
            print "\t0";
        }
    }
    print "\n";
}

sub read_bbh {
    my ($org, $file) = @_;

    open(FILE, "$file") || die "$!";
    while (<FILE>) {
        chomp;
        my @f = split(/\t/, $_);
        if (@f != 2) {
            die;
        }
        my ($prot1, $prot2) = @f;
        $ORTH{$prot1}{$org}{$prot2} = 1;
    }
    close(FILE);
}
