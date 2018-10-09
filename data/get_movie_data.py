#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Download movie data from OMDb API

import pandas as pd
import requests as r
import sys, json, codecs

def main():

	#read imdb links & api keys
	try:
		df = pd.read_csv('movielens/links.csv', dtype=str)
		with open('.api_keys.txt', 'r') as f:
			api_keys = f.readlines()
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

	#download movie data, 900 movies per api key
	#each api key is limited to 1000 movies per day
	movies = {}
	start = 0
	limit = 900
	for api_key in api_keys:
		for i in df['imdbId'][start:start + limit]:
			url = 'http://www.omdbapi.com/'
			payload = {'i': 'tt' + i, 'apikey': api_key.strip()}
			res = r.get(url, params=payload)
			if res.status_code == 200:
				movie = res.json()
				movies[i] = movie
		start += limit

	#output movie data to json file
	try:
		with open('movies-raw.json', 'wb') as f:
			json.dump(movies, codecs.getwriter('utf-8')(f), ensure_ascii=False)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

if __name__ == '__main__':
	main()
