#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Group movies into recommendation groups based on KMeans clustering

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
import sys, json, codecs, re, collections, random, pickle

def main():

	#read movie data
	try:
		with open('../data/movies-large.json', 'r') as f:
			all_movies = json.load(f)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

	#KMeans will run out of memory on full dataset
	n_movies = 1000
	n_clusters = int(n_movies / 10)
	random.seed(15)
	keys = random.sample(list(all_movies), n_movies)
	movies = {}
	for key in keys:
		movies[key] = all_movies[key]

	#extract only relevant movie data
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

	#group movies into clusters, along with their title and ID
	clusters = collections.defaultdict(list)
	cluster_numbers = {}
	i = 0
	for movie in movies:
		title = movies[movie]['Title']
		cluster_numbers[title] = kmeans[i]
		clusters[kmeans[i]].append({'title': title, 'id': movie})
		i += 1

	try:
		#serialize cluster data for future retrieval
		with open('clusters.pk', 'wb') as f:
			pickle.dump(clusters, f)
		with open('cluster-numbers.pk', 'wb') as f:
			pickle.dump(cluster_numbers, f)

		#output condensed dataset, containing only analysed movies
		with open('../data/movies-full.json', 'wb') as f:
			json.dump(movies, codecs.getwriter('utf-8')(f), ensure_ascii=False)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

#split data into tokens delimited by commas
def split(data):
	return re.split(r'\s*,\s*', data)

if __name__ == '__main__':
	main()
