#!/usr/bin/perl
use warnings; 
use strict;
use HTML::Parser;
use CGI qw(:standard);
use DBI;
use JSON;

# Database local
my $driver = "SQLite";
my $database = "database.db";
my $dsn = "DBI:$driver:dbname=$database";
my $userid = "";
my $password = "";
my $dbh = DBI->connect($dsn, $userid, $password, {RaiseError=> 1}) or die $DBI::errstr;

# Create CGI
my $cgi = new CGI;
print $cgi->header('text/html');

my $dateSetting = param('date') if (param('date'));
my $timeSetting = param('time') if (param('time'));
my $descriptionSetting = param('description') if (param('description'));

# Create new record, when  variable setting are detected
if ($dateSetting && $timeSetting && $descriptionSetting) 
{
    #this is an addition
	print $cgi->start_html(-title=>'NEW APPOINTMENT');
	print "Date: $dateSetting | Time: $timeSetting | Description: $descriptionSetting saved...";
	my $stmt = q/INSERT INTO appointments (date, time, desc) VALUES (?,?,?)/;
	my $sth = $dbh->prepare($stmt);
	$sth->execute($dateSetting, $timeSetting, $descriptionSetting);
	print "Done!";
	#back to main page
	print '<meta http-equiv="refresh" content="1;url=http://127.0.0.1/test/">';
} else 
{
    # this is a request
	my @output;
	my $sth = $dbh->prepare('select * from appointments'); 
	$sth -> execute;
	while(my $row = $sth->fetchrow_hashref) {
		push @output, $row;
	}
	print to_json({data=> \@output});
}
$dbh->disconnect();
