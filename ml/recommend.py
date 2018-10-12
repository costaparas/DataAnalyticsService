#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Retrieve recommendations for a given movie

import sys, random, pickle

def main():
	recommend()

def recommend():

	#retrieve cluster data
	try:
		with open('clusters.pk', 'rb') as f:
			clusters = pickle.load(f)
		with open('cluster-numbers.pk', 'rb') as f:
			cluster_numbers = pickle.load(f)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

	#movie to query
	if len(sys.argv) > 1:
		query = sys.argv[1]
	else:
		query = random.choice(list(cluster_numbers))

	status = 0
	if query in cluster_numbers:
		cluster = cluster_numbers[query]
		ret = {
			'movie_queried': query,
			'cluster_number': cluster,
			'cluster_movies': clusters[cluster]
		}
	else:
		ret = {'Unknown movie': query}
		status = 1
	print(ret)
	sys.exit(status)

if __name__ == '__main__':
	main()
