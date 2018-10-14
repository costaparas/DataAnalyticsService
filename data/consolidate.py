#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Append movie tags/keywords to movie data
#Cleanse movie awards information

import pandas as pd
import sys, re, json, codecs

def main():
	if len(sys.argv) != 3:
		print('Usage: %s INPUT-FILE OUTPUT-FILE' %sys.argv[0], file=sys.stderr)
		sys.exit(1)

	#read movie data, links and tags
	try:
		with open(sys.argv[1], 'r') as f:
			movies = json.load(f)
		links = pd.read_csv('movielens/links.csv', dtype=str)
		tags = pd.read_csv('movielens/tags.csv', dtype=str)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

	#append movie tags to movie data
	for index, row in tags.iterrows():
		link = links.query('movieId == "%s"' %row['movieId'])['imdbId'].to_string(index=False)
		if not link in movies: continue
		if not 'tags' in movies[link]: movies[link]['tags'] = []
		if not row['tag'] in movies[link]['tags']: movies[link]['tags'].append(row['tag'])

	#tidy awards info
	for movie in movies:
		terms = ['nomination', 'win']
		awards = movies[movie]['Awards']
		movies[movie]['Awards'] = {'wins': '0', 'nominations': '0'}
		for term in terms:
			m = re.search('(\d+)\s+%s' %term, awards)
			if m: movies[movie]['Awards'][term + 's'] = m.group(1)

	#output movie data to json file
	try:
		with open(sys.argv[2], 'wb') as f:
			json.dump(movies, codecs.getwriter('utf-8')(f), ensure_ascii=False)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

if __name__ == '__main__':
	main()
