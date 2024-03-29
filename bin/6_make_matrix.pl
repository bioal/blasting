#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM SPECIES_LIST GENE_REFSEQ
";

my %OPT;
getopts('p', \%OPT);

if (@ARGV != 2) {
    print STDERR $USAGE;
    exit 1;
}
my ($SPECIES_LIST, $GENE_REFSEQ) = @ARGV;

my @SPECIES = ();
open(SPECIES_LIST, "$SPECIES_LIST") || die "$!";
print "geneid";
while (<SPECIES_LIST>) {
    chomp;
    my @f = split("\t", $_);
    if ($f[0] =~ /^\d+$/) {
        my $id = $f[0];
        my $common_name = $f[3];
        push @SPECIES, $id;
        print "\t$id $common_name";
    }    
}
print "\n";
close(SPECIES_LIST);

my %GET_GENE_ID = ();
open(GENE_REFSEQ, "$GENE_REFSEQ") || die "$!";
while (<GENE_REFSEQ>) {
    chomp;
    my @f = split(/\t/, $_);
    my $geneid = $f[0];
    my $refseq_id = $f[1];
    $refseq_id =~ s/\.\d+//;
    $GET_GENE_ID{$refseq_id} = $geneid;
}
close(GENE_REFSEQ);

my %ORTH = ();
for (my $i=1; $i<@SPECIES; $i++) {
    read_bbh($SPECIES[$i], "$SPECIES[0]-$SPECIES[$i].bbh");
}

my %PARALOG = ();
open(PARALOG, "1.paralogs") || die "$!";
while (<PARALOG>) {
    chomp;
    my @f = split(/\t/, $_);
    if (@f != 2) {
        die;
    }
    my $query = $f[0];
    my $paralogs = $f[1];
    $PARALOG{$query} = $paralogs;
}
close(PARALOG);

### Print matrix
my $UNDEF_LINES = "";
my @PROT = keys %ORTH;
open(PIPE, "|sort -n") || die "$!";
for my $prot (sort @PROT) {
    print_matrix($prot);
}
close(PIPE);

print $UNDEF_LINES;

################################################################################
### Function ###################################################################
################################################################################

sub get_gene_id {
    my ($refseq_id) = @_;

    my $geneid = "0";
    $refseq_id =~ s/\.\d+//;
    if ($GET_GENE_ID{$refseq_id}) {
        $geneid = $GET_GENE_ID{$refseq_id};
    }

    return $geneid;
}

sub print_matrix {
    my ($prot) = @_;

    my $geneid = get_gene_id($prot);
    my $line = "$geneid\t$prot";
    if ($OPT{p}) {
        my $paralogs = $PARALOG{$prot} || "";
        $line .= "($paralogs)";
    }
    for (my $i=1; $i<@SPECIES; $i++) {
        my @hit = keys %{$ORTH{$prot}{$SPECIES[$i]}};
        if (@hit) {
            $line .= "\t". join(",", @hit);
        } else {
            $line .= "\t0";
        }
    }
    $line .= "\n";

    if ($geneid) {
        print PIPE $line;
    } else {
        $UNDEF_LINES .= $line;
    }
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
