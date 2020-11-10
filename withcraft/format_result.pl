#!/usr/bin/perl 
$str = do { local $/; <> };
($cleanStr = $str) =~ s/\n//g;
@F = split("\\\|", $cleanStr);
$i = 0;
$result = "";
for(; $i < $#F ; $i=$i+1){
    $result = $result."$F[$i]|";
}
print $result.$F[$#F]."\n";
