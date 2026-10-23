#!/bin/sh
# Build the paper with the same TinyTeX pdfLaTeX + BibTeX setup as ssn-group-papaer/workbench/*/paper/build.sh,
# in a scratch directory so the folder stays clean. Produces two PDFs:
#   main.pdf        anonymous review copy (\usepackage[review]{acl})
#   main_arxiv.pdf  non-anonymous preprint (\usepackage[preprint]{acl}) with the author block below
set -eu
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp -r "$here"/main.tex "$here"/appendix.tex "$here"/refs.bib "$here"/acl.sty "$here"/acl_natbib.bst \
      "$here"/figures "$here"/tables "$tmp"/
cd "$tmp"
sed -e 's/\\usepackage\[review\]{acl}/\\usepackage[preprint]{acl}/' \
    -e 's/\\author{Anonymous ACL submission}/\\author{Xiang Ding \\\\ Nagoya University \\\\ \\texttt{xiang.ding.i8@s.mail.nagoya-u.ac.jp}}/' \
    main.tex > main_arxiv.tex
for job in main main_arxiv; do
  pdflatex -interaction=nonstopmode -halt-on-error $job > /dev/null || { tail -30 $job.log; exit 1; }
  bibtex $job > bibtex_$job.log || true
  for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error $job > /dev/null || { grep -A5 "^!" $job.log; exit 1; }; done
  echo "== $job: $(pdfinfo $job.pdf | awk '/^Pages/ {print $2}') pages"
  grep -E "^!|LaTeX Error|undefined|Overfull" $job.log | sort | uniq -c || true
  grep -i -E "^warning|error" bibtex_$job.log || true
  cp $job.pdf "$here"/$job.pdf
done
