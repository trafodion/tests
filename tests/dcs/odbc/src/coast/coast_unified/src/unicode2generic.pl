use File::Basename;

$filename = ".";

if (-d $filename) {
	@files = ();
	opendir (DIR, $filename) || die "Can not open directory ".$filename;
	while (defined ($aFile = readdir(DIR))) {
#	    if ($aFile =~ m/.*\.[(cpp)|c|h]$/) {
	    if ($aFile =~ m/.*\.cpp$/) {
	        @files = (@files, $filename."\\".$aFile);
	    }
	}
	closedir(DIR);
}

$i = 0;
$j = 0;
my $str = "";
foreach $aFile (@files) {

    $str = "";
	print "====================================================================\n".$aFile."\n";
    open (FILE, $aFile) || die "Can not open file ".$aFile;
	$str = "";
    while (<FILE>) {
        $str .= $_;
    }
    close(FILE);
	while ($str =~ m/L"/mg) {
		$i++;
	}

	while ($str =~ s/(L)("[^"]*")/_T\($2\)/m) {
		print $1.$2."\n";
		$j++;
	}
	print "====================================================================\n";
	
	open(FILE, ">".$aFile) || die "Can not open file ".$aFile;
	print FILE $str;
	close(FILE);
}
print $i."\n";
print $j."\n";
