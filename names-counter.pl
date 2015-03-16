#!/usr/bin/perl
#
#         File:	names-counter
#     Abstract:	Count the number of unique names in names.csv DB.
#	 Usage:	names-counter [csv-data-file]
#     Data Fmt:	name,name,name...
#       Author:	Bill.Costa@unh.edu
#      Version: 20110311
#
#        Notes: Perl style comments and blank lines in the input
#		data stream are ignored.
#
#==============================================================================
#  Setup and Global Definitions  ==============================================
#==============================================================================

					#-- Pragmas ---------------------------
use warnings;				# Save me from my own dumb errors.
use strict;				# Keep things squeaky clean.
					#-- Core Modules ----------------------
use FindBin;				# Where the heck are we'z?


#==============================================================================
#  Subroutines  ===============================================================
#==============================================================================

sub commify 

#  Commify a number; "Perl Cookbook" 2.17

{
  my $text = reverse($_[0]);
  $text =~ s/(\d\d\d)(?=\d)(?!\d*\.)/$1,/g;
  return(scalar(reverse($text)));
}


#==============================================================================
#  Main Line  =================================================================
#==============================================================================

#-------------------------------+
# Get/find our input data file.	|
#-------------------------------+

my $dataName = $ARGV[0];
my $junk     = $ARGV[1];

die("? $0: too many arguments after '$dataName'\n") if (defined($junk));

$dataName = 'names.csv' if (not defined($dataName));

my $inSpec;
if (-e $dataName)
  {
    $inSpec = $dataName;
  }
else
  {
    $inSpec = "$FindBin::Bin/$dataName";
    die("? $0: cannot find input data\n_ $inSpec\n")
      if (not -e $inSpec);
  }

open(IN, "<$inSpec")
  or die("! $0: error opening $inSpec\n_ $!\n");


#-------------------------------+
# Parse each rec, stuff into a	|
# hash.				|
#-------------------------------+

my $NAME_RE = qr/^[a-z][a-z\.\-\ ]*$/i;
my %cat;

while (defined(my $ln = <IN>))
  {
    chomp($ln);
    chop($ln) if ($ln =~ m/\x0D/);	# Eat any trailing ^M too.
    $ln =~ s/#.*$//;			# Eat comments.
    next if ($ln =~ m/^\s*$/);		# Eat blank lines.

    foreach my $name (split(/,/, $ln))
      {
	if    ($name =~ m/^\s*$/)    { warn("- blank field line $. <$ln>\n")  }
	elsif ($name !~ m/$NAME_RE/) { warn("- invalid char line $. <$ln>\n") }
	else                         { $cat{$name}++;	                      }
      }
  }

close(IN);


#-------------------------------+
# Report name count and show	|
# most references.		|
#-------------------------------+

my $nameCnt = scalar(keys(%cat));
die("? $0: no names cataloged\n_ $inSpec\n_ ") if ($nameCnt <= 0);
print(commify($nameCnt), " unique names cataloged in $inSpec\n\n");

my $topLim = 5;
my $head = "Names referenced $topLim or more times:\n";

foreach my $name (sort { $cat{$b} <=> $cat{$a} } keys(%cat))
  {
    last if ($cat{$name} < $topLim);
    print($head);
    $head = '';
    printf("%8i: %s\n", $cat{$name}, $name);
  }

die("? $0: probable data err; no names found with $topLim or more refs\n_ ")
  if ($head ne '');


#==[ EOF: names-counter ]==
