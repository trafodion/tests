use File::Copy;
 
 print "Please enter user DataSource: ";
 chomp ($dsn = <STDIN>);

do {
	print "Please enter character set you want to test (ASCII, GB2, SJIS, LATIN1): ";
	 chomp ($charset = <STDIN>);
}
while ($charset !~ /^ASCII$/i && $charset !~ /^GB2$/i && $charset !~ /^SJIS$/i && $charset !~ /^LATIN1$/i);

$user = "odbcqa";
$pwd = "odbcqa";
$workinglocation = "\\\\cacphanhai\\HPAT\\Programs\\UNICODE\\TCSCOAST_ImplicitCasting\\MVS 2005 Project files\\bin\\";
$PC = $ENV{"COMPUTERNAME"};
$exe = "COAST.EXE";
$encode = "encode.pl";

mkdir($workinglocation.$PC) || die "Error create direcotory ".$workinglocation.$PC."\n" unless (-e $workinglocation.$PC);
copy($workinglocation.$exe,$workinglocation.$PC."\\".$exe) or die "Copy failed: $!";
copy($workinglocation.$encode,$workinglocation.$PC."\\".$encode) or die "Copy failed: $!";

#system ("perl \"".$workinglocation.$PC."\\".$encode."\" ".$charset."") unless (-e "charset_auto_generated_".$charset.".char");

#exit;

open (OUT, ">run.bat") || die "Fails to create a batch file!\n";
print OUT "\@echo ON\n";
print OUT "set ODBC_REGRESSION_WORKING_DIR=\"".$workinglocation.$PC."\"\n";
print OUT "rem Convert base text script into an executable perl script\n";
print OUT "rem perl conversion.pl > encode.pl\n";
print OUT "rem perl encode.pl " . $charset . "\n";
print OUT "rem COAST.EXE -d " . $dsn . " -c " . $charset . "\n";
print OUT "set\n";
print OUT "pause\n";
close(OUT);

system("run.bat");
