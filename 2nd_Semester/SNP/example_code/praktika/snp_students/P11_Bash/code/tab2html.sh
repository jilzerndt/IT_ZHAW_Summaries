#!/bin/bash

# produces a crude HTML table from a tabular file (given on stdin) with columns separated by ":"
# usage: tab2html < inbut.txt > output.html

awk $* -- '
BEGIN {
   FS=":"   # field-separator: which character separats fields in a record (i.e. in a line)
   print "<!DOCTYPE html>"
   print "<html>"
   print "  <head>"
   print "    <style>"
   print "      table{border:1px solid black;border-collapse:collapse;}"
   print "      tr:nth-child(even){background-color: #f2f2f2;}"
   print "      td{border:1px solid black;padding:15px;}"
   print "    </style>"
   print "    <title>Tabular Data</title>"
   print "  </head>"
   print "  <body>"
   print "    <div style=\"overflow-x:auto;\">"
   print "      <table>"
}
{
   print "        <tr>"
   for (i = 1; i <= NF; i++) { print "          <td>"$i"</td>" }
   print "        </tr>"
}
END {
    print "      </table>"
    print "    </div>"
    print "  </body>"
    print "</html>"
}
'

