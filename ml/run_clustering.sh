#!/bin/sh

prog='python3 clustering.py'

for model in KMEANS MEANSHIFT BIRCH AGGLOMERATIVE AGGLOMERATIVE_EUCLID AGGLOMERATIVE_L1 AGGLOMERATIVE_L2 AGGLOMERATIVE_MAN
do
	test $model = 'MEANSHIFT' && $prog $model && continue
	for n_clusters in 100 150 200 250 300 350 400
	do
		if echo $model | egrep -q '^AGGLOMERATIVE'
		then
			for linkage in average complete
			do
				$prog $model $n_clusters $linkage
			done
		else
			$prog $model $n_clusters
		fi
	done
done

while read -r line
do
	echo "$line" | sed -r 's/\s{2,}/,/g;s/,$//' >> metrics.csv
done < metrics.txt
