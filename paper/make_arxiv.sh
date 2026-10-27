#!/bin/sh
# Package the non-anonymous preprint as an arXiv TeX source upload: arxiv_source.tar.gz.
# main.tex is the preprint version (as main_arxiv.tex in build.sh) with \pdfoutput=1 on line 1 and comment lines removed.
# arXiv does not run BibTeX, so the bibliography is shipped as main.bbl. Only the figures and tables the paper uses
# are included. The package is test-compiled from a clean copy with pdfLaTeX alone, as arXiv does.
set -eu
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
src="$tmp/src"
mkdir -p "$src/figures" "$src/tables"
{
  echo '\pdfoutput=1'
  sed -e '/^[[:space:]]*%/d' \
      -e 's/\\usepackage\[review\]{acl}/\\usepackage[preprint]{acl}/' \
      -e 's/\\author{Anonymous ACL submission}/\\author{Xiang Ding \\\\ Nagoya University \\\\ \\texttt{xiang.ding.i8@s.mail.nagoya-u.ac.jp}}/' \
      "$here/main.tex"
} > "$src/main.tex"
sed -e '/^[[:space:]]*%/d' "$here/appendix.tex" > "$src/appendix.tex"
cp "$here/acl.sty" "$here/acl_natbib.bst" "$src/"
for f in $(grep -ho 'figures/[A-Za-z0-9_]*' "$src/main.tex" "$src/appendix.tex" | sort -u); do cp "$here/$f.pdf" "$src/$f.pdf"; done
for f in $(grep -ho 'tables/[A-Za-z0-9_]*\.tex' "$src/main.tex" "$src/appendix.tex" | sort -u); do cp "$here/$f" "$src/$f"; done
# bibliography: run BibTeX once in a scratch copy, keep only the .bbl
work="$tmp/work"
cp -r "$src" "$work"
cp "$here/refs.bib" "$work/"
cd "$work"
pdflatex -interaction=nonstopmode -halt-on-error main > /dev/null
bibtex main > /dev/null
cp main.bbl "$src/main.bbl"
# test: clean copy, pdfLaTeX only
test="$tmp/test"
cp -r "$src" "$test"
cd "$test"
for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error main > /dev/null || { grep -A5 "^!" main.log; exit 1; }; done
grep -E "undefined|Overfull" main.log | sort | uniq -c || true
echo "test build: $(pdfinfo main.pdf | awk '/^Pages/ {print $2}') pages"
cp main.pdf "$tmp/check.pdf"
cd "$src"
tar -czf "$here/arxiv_source.tar.gz" *
cd "$here"
echo "wrote arxiv_source.tar.gz:"
tar -tzf arxiv_source.tar.gz
# the test build must match the preprint built by build.sh
if [ -f main_arxiv.pdf ]; then
  a=$(pdftotext "$tmp/check.pdf" - | md5sum | cut -c1-32)
  b=$(pdftotext main_arxiv.pdf - | md5sum | cut -c1-32)
  [ "$a" = "$b" ] && echo "text identical to main_arxiv.pdf" || echo "WARNING: text differs from main_arxiv.pdf (rerun build.sh?)"
fi
