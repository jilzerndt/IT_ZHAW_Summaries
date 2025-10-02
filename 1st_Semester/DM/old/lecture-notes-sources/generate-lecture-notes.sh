#!/bin/sh

echo "Building graphs with graphviz"
dot -Tpng graphviz/maxmingraph.dot -o graphviz/maxmingraph.png || exit 1
dot -Tpng graphviz/g1.dot -o graphviz/g1.png || exit 1
dot -Tpng graphviz/g2.dot -o graphviz/g2.png || exit 1

echo "Compiling lecture notes with solutions"
latexmk -pdf lecture-notes-with-solutions.tex || exit 1
echo "Compiling lecture notes without solutions"
latexmk -pdf lecture-notes-without-solutions.tex || exit 1

echo "Cleaning up lecture-notes-sources"
rm *.aux
rm *.bbl
rm *.blg
rm *.fdb_latexmk
rm *.fls
rm *.log
rm *.toc

echo "Deploying lecture notes"
mkdir -p ../dist/lecture-notes
mv lecture-notes-with-solutions.pdf ../dist/lecture-notes
mv lecture-notes-without-solutions.pdf ../dist/lecture-notes