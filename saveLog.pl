use strict;
use warnings;
use utf8;
use Encode;
use File::Copy 'copy';

my $frmtxt = $ARGV[0];
my $frmsvg = $ARGV[1];


my $width = 10;
my $height = 10;
my $readline = 0;
my $gene = 0;
my $run = 0;
my @column;
my @field;

open( my $fh, "<", $frmtxt)
	or die "Cannot open $frmtxt: $!";
while( my $line = readline($fh)){
	@column = split(/\t/, $line);
	if( $column[0] eq 'gene')
	{
		$gene = int($column[1]);
	}
	elsif( $column[0] eq 'run')
	{
		$run = int($column[1]);
	}
}
close $fh;

my $dir = sprintf("./stateLogs/%08d", $run);
my $totxt = sprintf("$dir/%08d.txt", $gene);
copy($frmtxt, $totxt)
	or die "Can't copy $frmtxt to $totxt:$!";

open($fh, "<", $frmsvg)
	or die "Cannot open $frmsvg: $!";
my $tosvg = sprintf("$dir/%08d.svg", $gene);
copy($frmsvg, $tosvg)
	or die "Can't copy $frmsvg to $tosvg:$!";

#copy to ~/www directory
$dir = sprintf("/home/ikatake/www/wetsteam/LifeGameBotBS/stateLogs/%08d", $run);
$totxt = sprintf("$dir/%08d.txt", $gene);
copy($frmtxt, $totxt)
	or die "Can't copy $frmtxt to $totxt:$!";
$tosvg = sprintf("$dir/%08d.svg", $gene);
copy($frmsvg, $tosvg)
	or die "Can't copy $frmsvg to $tosvg:$!";


exit(0);

