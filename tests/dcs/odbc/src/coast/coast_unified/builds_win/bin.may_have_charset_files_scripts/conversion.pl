# @@@ START COPYRIGHT @@@
#
# (C) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# @@@ END COPYRIGHT @@@


$basescript = "charset_ascii_base.char"; 

open (FILE, $basescript) || die "Can not open file ".$basescript;
$str = "";
while (<FILE>) {
	$str .= $_;
}
close(FILE);

print "use Encode;\n\n";

print "die \"Wong argument!\\nUsage: encode.pl charset\\ncharset: ASCII|LATIN1|SJIS|GBK(GB2)\" if (\$#ARGV != 0);\n\n";

print "\$language = \$ARGV[0];\n";
print "\$unicodefile = \"\";\n";
print "\$codePage = \"\";\n";
print "\$charsetScript = \"\";\n";
print "\$delimited = \"\\\"\";\n";
print "if (\$language =~ /\^ASCII\$/i) {\n";
print "		\$unicodefile = \"ASCII_8859-1.TXT\";\n";
print "		\$codePage = \"cp1252\";\n";
print "		\$charsetScript = \"charset_auto_generated_ascii.char\";\n";
print "		\$delimited = \"\";\n";
print "}\n";
print "elsif (\$language =~ /\^LATIN1\$/i) {\n";
print "		\$unicodefile = \"LATIN_8859-1.TXT\";\n";
print "		\$codePage = \"cp1252\";\n";
print "		\$charsetScript = \"charset_auto_generated_latin1.char\";\n";
print "}\n";
print "elsif (\$language =~ /\^SJIS\$/i) {\n";
print "		\$unicodefile = \"SJIS_CP932.TXT\";\n";
print "		\$codePage = \"cp932\";\n";
print "		\$charsetScript = \"charset_auto_generated_sjis.char\";\n";
print "}\n";
print "elsif (\$language =~ /\^GBK|GB2\$/i) {\n";
print "		\$unicodefile = \"GBK_CP936.TXT\";\n";
print "		\$codePage = \"cp936\";\n";
print "		\$charsetScript = \"charset_auto_generated_gb2.char\";\n";
print "}\n";
print "else {\n";
print "		print \"Wong argument!\\nUsage: encode.pl charset\\ncharset: ASCII|LATIN1|SJIS|GBK(GB2)\";\n";
print "		exit(0);\n";
print "}\n\n";

print "\$identifierSize = 10;\n";
print "\$str = \"\";\n";
print "\$indexI = 0;\n";
print "\$indexL = 0;\n\n";

print "if (-f \$unicodefile) {\n";
print "		open (FILE, \$unicodefile) || die \"Can not open file \".\$unicodefile;\n";
print "		\$i = 0;\n";
print "		while (<FILE>) {\n";
print "			if (\$_ =~ m/^0x.+\\s+(0x....)\\s+\\S+/s) {\n";
print "				\$str .= chr(hex(\$1));\n";
print "				\$i++;\n";
print "			}\n";
print "		}\n";
print "		close(FILE);\n";
print "}\n\n";

print "shuffle();\n";
print "resetIndex();\n";
print "generate_script();\n\n";

print "sub shuffle\n";
print "{\n";
print "		my \$temp = \"\";\n";
print "		my \@arr = split(//, \$str);\n";
print "		for (\$i = \$#arr; \$i>0; \$i--) {\n";
print "			\$j = int(rand(\$i));\n";
print "			\$temp = \$arr[\$i];\n";
print "			\$arr[\$i] = \$arr[\$j];\n";
print "			\$arr[\$j] = \$temp;\n";
print "		}\n";
print "		\$str = join('', \@arr);\n";
print "}\n\n";

print "sub resetIndex\n";
print "{\n";
print "		\$indexI = int(rand(length(\$str)));\n";
print "		\$indexL = int(rand(length(\$str)));\n";
print "}\n\n";

print "#Return the next Identifer\n";
print "sub nextI\n";
print "{\n";
print "		my(\$size,\$encoded) = \@_;\n";
print "		my \$myIdentifier = \"\";\n";
print "		\$size = \$identifierSize if (\$size =~ /\^\$/);\n\n";
print "		while (1) {\n";
print "			\$myIdentifier = \"\";\n";
print "			if (\$language !~ /\^ASCII\$/i) {\n";
print "				\$myIdentifier = getToken(\$size, \"I\");\n";
print "			}\n";
print "			else {\n";
print "				while (length(\$myIdentifier) < \$size) {\n";
print "					my \$aChar = getToken(1, \"I\");\n";
print "					next if (\$myIdentifier =~ /\^\$/ and \$aChar !~ /\^[a-zA-Z]\$/);\n";
print "					\$myIdentifier .= \$aChar if (\$aChar =~ /\^[\\w\\d]\$/);\n";
print "				}\n";
print "				\$myIdentifier = uc(\$myIdentifier);\n";
print "			}\n";
print "			if (\$duplicate{\$myIdentifier} =~ /\^\$/) {\n";
print "				\$duplicate{\$myIdentifier} = \"YES\";\n";
print "				last;\n";
print "			}\n";
print "			else {\n";
print "				shuffle();\n";
print "			}\n";
print "		}\n";
print "		if (\$encoded =~ /\^no\$/i) {\n";
print "			return \$myIdentifier;\n";
print "		}\n";
print "		else {\n";
print "			return encode(\$codePage, \$myIdentifier);\n";
print "		}\n";
print "}\n\n";

print "#Return the next Literal with size in byte\n";
print "sub nextLByte\n";
print "{\n";
print "		my(\$literalSize) = \@_;\n";
print "		my \$literalByte = getToken(\$literalSize, \"L\");\n";
print "		my \$flag = 1;\n";
print "		my \$count = 0;\n";
print "		while (\$flag == 1) {\n";
print "			\$count = length(encode_utf8(\$literalByte));\n";
print "			\$flag = 0 if (\$count <= \$literalSize);\n";
print "			if (\$flag == 1) {\n";
print "				\$literalByte =~ s/.\$//;\n";
print "				\$indexL--;\n";
print "			}\n";
print "		}\n";
print "		my \@arr = (encode(\$codePage, \$literalByte), \$count);\n";
print "		return \\\@arr;\n";
print "}\n\n";

print "#Return the next Literal in char\n";
print "sub nextLChar\n";
print "{\n";
print "		my(\$literalSize) = \@_;\n";
print "		my \$literalChar = getToken(\$literalSize, \"L\");\n";
print "		my \@arr = (encode(\$codePage, \$literalChar), length(\$literalChar));\n";
print "		return \\\@arr;\n";
print "}\n\n";

print "#Get nextToken\n";
print "sub getToken\n";
print "{\n";
print "		my(\$size,\$type) = \@_;\n";
print "		my \$token = \"\";\n\n";
print "		my \$index = \$indexL;\n";
print "		\$index = \$indexI if (\$type =~ /\^I\$/);\n\n";
print "		if (\$index < (length(\$str) - \$size))\n";
print "		{\n";
print "			\$token = substr \$str, \$index, \$size;\n";
print "			\$index += \$size;\n";
print "		}\n";
print "		else\n";
print "		{\n";
print "			\$token = substr \$str, \$index;\n";
print "			\$index = \$size - length(\$token);\n";
print "			\$token .= substr \$str, 0, \$index;\n";
print "		}\n";
print "		if (\$type =~ /\^I\$/) { #Identifier\n";
print "			\$token =~ s/^[\\s+\\\$]//;\n";
print "			\$token =~ s/\\s+\$//;\n";
print "			\$token =~ s/[\\.\\\\\\\/\\@\\^\"]//g; #Hate to use 'double quote' character as identifier\n";
print "			\$indexI = \$index;\n";
print "		}\n";
print "		else { # Literal\n";
print "			\$token =~ s/'/./g; #Hate to insert 'quote' character as data\n";
print "			\$indexL = \$index;\n";
print "		}\n";
print "		return \$token;\n";
print "}\n\n";

print "#Translate identifiers to wildcards\n";
print "sub wctranslate\n";
print "{\n";
print "		my (\$src, \$dest, \$val) = \@_;\n";
print "		\@src_arr = split(//, \$src);\n";
print "		\@dest_arr = split(//, \$dest);\n";
print "		\@val_arr = split(//, \$val);\n";
print "		my \$i = 0;\n";
print "		foreach my \$aChar (\@dest_arr) {\n";
print "			my \$temp = \$src_arr[\$i];\n";
print "			if ((\$aChar =~ /\^\\w\$/) && (\$aChar =~ /\^\$temp\$/)) {\n";
print "				\$dest_arr[\$i] = \$val_arr[\$i];\n";
print "			}\n";
print "			elsif (\$aChar =~ /\^\\.\$/) {\n";
print "				\$dest_arr[\$i] = \"\";\n";
print "			}\n";
print "			else {\n";
print "			}\n";
print "			\$i++;\n";
print "		}\n";
print "		return encode(\$codePage, join('',\@dest_arr));\n";
print "}\n\n";

print "#Get spaces\n";
print "sub spaces\n";
print "{\n";
print "		my (\$sp) = \@_;\n";
print "		my \$str = \"\";\n";
print "		return \$str if (\$sp <= 0);\n";
print "		for (my \$i=0; \$i<\$sp; \$i++) {\$str .= \" \";}\n";
print "		return \$str;\n";
print "}\n\n";

print "sub generate_script\n";
print "{\n";
print "\topen (OUT, \">\".\$charsetScript) || die \"Can not open outfile\\n\";\n";

$str =~ s/_ISO88591//g;
$str =~ s/(\\|")/\\$1/g;

@apis = split(/\[END\]/, $str);
foreach my $myApi (@apis) {
	next if ($myApi =~ /^\s+$/);
	
	if ($myApi =~ /^--/) {
		print "\tprint OUT \"".$myApi."\".\"\\n\";\n\n";
		print "\tprint OUT \"[END]\".\"\\n\";\n\n";
		next;
	}
	
	%h = ();
	
	# Find and replace COLUMN NAME
	while ($myApi =~ m/(C\d+)([^\w+_])/gi) {
		my $col = uc $1;
		if ($h{$col} =~ m/^$/)
		{
			$h{$col} = "\$delimited . nextI() . \$delimited;";
		}
	}
	$myApi =~ s/C(\d+)([^\w+_])/" . \$h{\"C$1\"} . "$2/gi;
	
	# Find and replace TABLE NAME
	while ($myApi =~ m/(TABLE_NAME\d+)(_(\d+))*/g) {
		my $col = $1;
		my $size = $3;
		if ($h{$col} =~ m/^$/)
		{
			$h{$col} = "nextI(" . $size . ");";
		}
	}

	$myApi =~ s/(TABLE_NAME\d+)(_(\D)|_\d+)*/" . \$delimited . \$h{\"$1\"} . "$3" . \$delimited . "/g;

	# Find and replace  WILDCARD
	$counter = 0;
	while ($myApi =~ m/(WILDCARD_)([^\|]+)\|([^\s|\\|\"]+)/g) {
		my $key = $1;
		my $source = $2;
		my $wc = $3;
		if ($h{$key.$source} =~ m/^$/)
		{
			$h{$key.$source} = "nextI(" . length($source) . ",\"no\");";
		}
		$h{$key.$source} .= "\n\t\$wc[" . $counter .
							"] = \$delimited . wctranslate(\"" . $source .
							"\",\"" . $wc . "\",\$h{\"" . $key.$source . "\"}). \$delimited;";
		$counter++;
	}
	
	$counter = 0;
	$counter++ while ($myApi =~ s/WILDCARD_[^\|]+\|[^\s|\\|\"]+/" . \$wc[$counter] . "/);

	# Find and replace  DATA
	while ($myApi =~ m/(B?)(LITERAL\d+_)(\d+)/g) {
		my $inByte = $1;
		my $data = $1.$2.$3;
		my $size = $3;
		if ($h{$data} =~ m/^$/)
		{
			if ($inByte =~ /^$/) {
				$h{$data} = "nextLChar(" . $size . ");";
			}
			else {
				$h{$data} = "nextLByte(" . $size . ");";
			}
		}
	}
	$myApi =~ s/(B?LITERAL\d+_\d+)(_(\d+))*/" . \$h{\"$1\"}[0] . spaces($3 - \$h{\"$1\"}[1]) . "/g;

	print "\t\%h = ();\n";
	print "\t\%duplicate = ();\n";
	print "\t\@wc = ();\n";
	
	foreach my $key (sort (keys %h)) {
		print "\t\$h\{\"".$key."\"\} = ".$h{$key}."\n";
	}
	print "\n";
	
	foreach (split(/\n/, $myApi)) {
		print "\tprint OUT \"" . $_ . "\".\"\\n\";\n";
	}
	print "\tprint OUT \"[END]\".\"\\n\";\n\n";
}

print "\tclose (OUT);\n";
print "}\n";
