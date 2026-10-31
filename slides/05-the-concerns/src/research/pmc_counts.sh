#!/bin/bash
# Query NCBI E-utilities esearch (db=pmc) for article counts by license filter; saves raw JSON.
OUT="$1"; mkdir -p "$OUT"
declare -A Q
Q[all_pmc]='all[sb]'
Q[oa_or_am]='(open_access[Filter] OR author_manuscript[Filter])'
Q[open_access]='open_access[Filter]'
Q[author_manuscript]='author_manuscript[Filter]'
Q[commercial_ok]='(cc0_license[Filter] OR cc_by_license[Filter] OR cc_by-sa_license[Filter] OR cc_by-nd_license[Filter]) AND (open_access[Filter] OR author_manuscript[Filter])'
Q[noncommercial_only]='(cc_by-nc_license[Filter] OR cc_by-nc-nd_license[Filter] OR cc_by-nc-sa_license[Filter]) AND (open_access[Filter] OR author_manuscript[Filter])'
Q[cc_by]='cc_by_license[Filter]'
Q[cc0]='cc0_license[Filter]'
for k in all_pmc oa_or_am open_access author_manuscript commercial_ok noncommercial_only cc_by cc0; do
  curl -sS -G "https://eutils.ncbi.nlm.nih.gov/eutils/esearch.fcgi" --data-urlencode "db=pmc" --data-urlencode "term=${Q[$k]}" --data-urlencode "retmax=0" --data-urlencode "retmode=json" -o "$OUT/esearch_pmc_${k}.json"
  echo "$k	$(date -u +%FT%TZ)	${Q[$k]}" >> "$OUT/queries.tsv"
  sleep 1
done
