#!/usr/bin/env perl

## Nickname lookup
## Example code for parsing a csv file of names and nicknames
## into a hash dictionary for quick lookups
##
## Expects a csv where each line contains a list of related names
## EX: 
## abbie,abby,abigail
## beth,betsy,betty,elizabeth

use strict;

use Getopt::Std;

my $opts = {};
getopts('hd', $opts);

if (!$ARGV[0] or $opts->{h}) {
	usage();
	exit;
}

my $name_dict;

# Open the input file and output file
open my $in_file , '<', $ARGV[0] or die "Cant open $ARGV[0]";

while(defined(my $line = <$in_file>)) {

	$line =~ s/^\s*|\s*$//g; # strip leading and following whitespace
	$line =~ s/#.*$//;	# strip comments

	if (!$line or $line =~ /^,+$/ or $line =~ /^\s*$/) {
		# line is blank
		next;
	}

	my @names = split(',', $line);
	for my $name (@names) {
		if ($name !~ /^[a-z\.\-\ ']*$/i) {
			# Invalid character found
			warn "Invalid character at line $. : $line\n";
		}
		elsif ($name =~ /^\s*$/) {
			warn "Blank field at line $. : $line\n";
		}
		else {
			foreach (@names) {
				unless ($_ eq $name) {
					$name_dict->{$name}->{$_} = 1;
				}
			}
		}
	}
}

close $in_file;

if ($opts->{d}) {
	print "The dictionary contains: \n";
	for my $name (sort keys %$name_dict) {
		print "$name => " . join(', ', sort keys %{$name_dict->{$name}}) . "\n";
	}
	exit;
}

my $lookup = lc $ARGV[1];
unless ($name_dict->{$lookup}) {
	print "No nicknames found for the name $ARGV[1]\n";
	exit;
}

print "The nicknames for $ARGV[1] are: " . join(', ', sort keys %{$name_dict->{$lookup}}) . "\n";

sub usage {
	print <<"EOF";

Usage: name_lookup.pl [options] <names_file_path> <name>

Example:

	./name_lookup.pl ./names.csv Dan

Options:
	-h 		Help. Print this screen.
	-d 		Dump the name dictionary.

EOF
}

