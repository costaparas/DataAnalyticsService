#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Drop any movies in the dataset that are "unreasonable"

import sys, re, json, codecs

debug = True

def main():
	#read in possibly "tainted" movie dataset
	try:
		with open('movies-large.json', 'r', encoding='utf-8') as f:
			movies = json.load(f)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

	#remaining "valid" movies will be exported at the end
	good_movies = {}

	for movie in movies:
		dat = movies[movie]

		#firstly, ignore all non-movie entries
		if dat['Type'] != 'movie':
			print_err(movie, 'Type', dat['Type'])
			continue

		#ignore all movies with important fields that are invalid or missing
		if not re.match(r'^\d+\.\d+$', dat['imdbRating']):
			print_err(movie, 'imdbRating', dat['imdbRating'])
			continue
		elif not re.match(r'^tt\d{4,}', dat['imdbID']):
			print_err(movie, 'imdbID', dat['imdbID'])
			continue
		elif not re.match(r'^\d{4}$', dat['Year']):
			print_err(movie, 'Year', dat['Year'])
			continue
		elif not re.match(r'^http', dat['Poster']):
			print_err(movie, 'Poster', dat['Poster'])
			continue
		elif not re.match(r'^\d{2} [A-Z][a-z]{2} \d{4}$', dat['Released']):
			print_err(movie, 'Released', dat['Released'])
			continue
		if not re.match(r'^\d+ min$', dat['Runtime']):
			print_err(movie, 'Runtime', dat['Runtime'])
			continue

		#drop the word "votes" from the end of some votes
		if not re.match(r'^\d+(,\d+)*$', dat['imdbVotes']):
			dat['imdbVotes'] = dat['imdbVotes'].replace(' votes', '')
			if not re.match(r'^\d+(,\d+)*$', dat['imdbVotes']):
				print_err(movie, 'imdbVotes', dat['imdbVotes'])
				continue

		#format of bad titles deduced using the following approach
		'''
		if not (len(dat['Title']) > 12
			or re.match(r'^[\w\ \.\,\-\&\'\!\?\*\/\:\(\)\[\]]{4,}$', dat['Title'], re.IGNORECASE)
			or re.match(r'^[a-z0-9]+$', dat['Title'], re.IGNORECASE)):
			print(dat['Title'])
		'''

		#drop of movies with title "#DUPE#"
		if dat['Title'] == '#DUPE#':
			print_err(movie, 'Title', dat['Title'])
			continue

		#drop movies with bad data for directors, writers, actors
		for field in ['Director', 'Writer', 'Actors']:
			if re.match(r'^(N/A|\s*)$', dat[field]):
				print_err(movie, dat[field], field)
				continue

		#drop movies with short plots
		if len(dat['Plot']) < 10:
			print_err(movie, 'Plot', dat['Plot'])
			continue

		#about 1,000 movies have "N/A", "UNRATED" or "NOT RATED"
		#but these can be worked with, so don't drop
		#print(dat['Rated'])

		#all genres after above filtering appear to be valid
		#print(dat['Genre'])

		good_movies[movie] = dat

	#output remaining "valid", usable movies
	try:
		with open('movies-full.json', 'wb') as f:
			json.dump(good_movies, codecs.getwriter('utf-8')(f), ensure_ascii=False)
	except (PermissionError, OSError) as e:
		print(str(e), file=sys.stderr)
		sys.exit(1)

	if debug:
		invalid = len(movies) - len(good_movies)
		print('Total: %d, invalid: %d, valid: %d' %(len(movies), invalid, len(good_movies)))

def print_err(movie, name, value):
	if debug:
		print('Dropping %s due to invalid "%s": %s' %(movie, name, value))

if __name__ == '__main__':
	main()
