#!/usr/bin/perl -w
use strict;
use File::Basename;
use Getopt::Std;
my $PROGRAM = basename $0;
my $USAGE=
"Usage: $PROGRAM PROTEOME_LIST_FILE
";

my %OPT;
getopts('', \%OPT);

if (!@ARGV) {
    print STDERR $USAGE;
    exit 1;
}
my ($LIST_FILE) = @ARGV;

my %INFO;
open(LIST, $LIST_FILE) || die;
while (<LIST>) {
    chomp;
    my ($proteome_id, $taxid, $oscode, $superkingdom, $num_canonical, $num_isoforms, $num_mapping, $name) = split(/\t/, $_);
    $INFO{$proteome_id} = {taxid => $taxid, oscode => $oscode, name => $name};
}
close(LIST);

my @DIRS = ('Bacteria', 'Archaea', 'Eukaryota');
for my $dir (@DIRS) {
    for my $f (<$dir/*.fasta>) {
        next if ($f =~ /_DNA/);
        next if ($f =~ /_additional/);
        read_seqfile($f);
    }
}

################################################################################
### Functions ##################################################################
################################################################################
sub read_seqfile {
    my ($f) = @_;

    if ($f =~ /(UP\d+)_(\d+)/) {
        my ($proteome_id, $taxid) = ($1, $2);
        my $oscode = $INFO{$proteome_id}->{oscode};
        # $oscode = lc($oscode);
        open(F, $f) || die;
        while (<F>) {
            if (/^>(\S+) (\S.*)$/) {
                my ($name, $title) = ($1, $2);
                my ($db, $acc, $entid) = split(/\|/, $name);
                print ">${oscode}:$acc $title\n";
            } else {
                print;
            }
        }
        close(F);
    } else {
        print STDERR "ERROR: file name format error\n";
        die;
    }    
}
