#!/bin/sh

prog='python3 clustering.py'
rm -f metrics.txt metrics.csv

for model in KMEANS MEANSHIFT BIRCH AGGLOMERATIVE AGGLOMERATIVE_EUCLID AGGLOMERATIVE_L1 AGGLOMERATIVE_L2 AGGLOMERATIVE_MAN
do
	printf "%s" $model
	test $model = 'MEANSHIFT' && printf "\n" && $prog $model && continue
	for n_clusters in 100 150 200 250 300 350 400
	do
		if printf "%s" "$model" | egrep -q '^AGGLOMERATIVE'
		then
			for linkage in average complete
			do
				printf " %s" "$n_clusters ($linkage)"
				$prog $model $n_clusters $linkage
			done
		else
			printf " %s" "$n_clusters"
			$prog $model $n_clusters
		fi
	done
	printf "\n"
done

while read -r line
do
	printf "%s\n" "$line" | sed -r 's/\s{2,}/,/g;s/,$//' >> metrics.csv
done < metrics.txt
