#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Group movies into recommendation groups based on KMeans clustering

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
import sys, json, codecs, re, collections, random

def main():

	#read movie data
	try:
		with open('../data/movies-full.json', 'r') as f:
			all_movies = json.load(f)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

	#KMeans will run out of memory on full dataset
	n_movies = 1000
	n_clusters = int(n_movies / 10)
	keys = random.sample(list(all_movies), n_movies)
	movies = {}
	for key in keys:
		movies[key] = all_movies[key]

	genres = []
	directors = []
	actors = []
	for movie in movies:
		genres.append(movies[movie]['Genre'])
		directors.append(movies[movie]['Director'])
		actors.append(movies[movie]['Actors'])

	genre_vectorizer = CountVectorizer(tokenizer=split)
	genres_vectorized = genre_vectorizer.fit_transform(genres)
	#print(genre_vectorizer.get_feature_names())

	director_vectorizer = CountVectorizer(tokenizer=split)
	directors_vectorized = director_vectorizer.fit_transform(directors)
	#print(director_vectorizer.get_feature_names())

	actor_vectorizer = CountVectorizer(tokenizer=split)
	actors_vectorized = actor_vectorizer.fit_transform(actors)
	#print(actor_vectorizer.get_feature_names())

	cluster_features = np.hstack([
		genres_vectorized.todense(),
		directors_vectorized.todense(),
		actors_vectorized.todense()
	])

	kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit_predict(cluster_features)
	#print(kmeans)
	clusters = collections.defaultdict(list)
	cluster_numbers = {}
	i = 0
	for movie in movies:
		title = movies[movie]['Title']
		cluster_numbers[title] = kmeans[i]
		clusters[kmeans[i]].append(title)
		i += 1
	#for mov in clusters: print(mov, clusters[mov])

	query = random.choice(list(cluster_numbers))
	if query in cluster_numbers:
		cluster = cluster_numbers[query]
		print('cluster:', cluster)
		print('movies:', clusters[cluster])

def split(to_split):
	return re.split(r'\s*,\s*', to_split)

if __name__ == '__main__':
	main()
