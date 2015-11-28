#/bin/bash -eu
 
end=2017
a=年生
for i in $(seq 1901 ${end}) ; do
  gzcat ~/Downloads/jwiki/wiki_categoty.txt.gz | grep  -E "$i$a" | head -n 10;
done