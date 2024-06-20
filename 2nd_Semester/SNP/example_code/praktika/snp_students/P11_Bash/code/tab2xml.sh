#!/bin/bash

# produces an XML file from a tabular file (given on stdin) with columns separated by ":"
# usage: tab2xml < inbut.txt > output.xml

awk $* -- '
BEGIN {
   FS=":"   # field-separator: which character separats fields in a record (i.e. in a line)
   print "<?xml version=\"1.0\" standalone=\"yes\"?>"
   print "<Table>"
}
{
   print " <Row>"
   for (i = 1; i <= NF; i++) { print "  <Col>"$i"</Col>" }
   print " </Row>"
}
END {
    print "</Table>"
}
'

