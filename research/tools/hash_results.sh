#!/bin/bash
# Record SHA-256 of raw score files for each garden-path experiment (raw files are gitignored).
cd "$(dirname "$0")/../.."
for d in results/gp/E*/; do
  (cd "$d" && ls *.scores.csv.gz >/dev/null 2>&1 && sha256sum *.scores.csv.gz > MANIFEST.sha256)
done
