FILE SUMMARY
============

* `clustering.py`: perform a KMeans clustering on the movie dataset
* `cluster-numbers.pk`: serialized Python object containing a mapping of movie titles to cluster numbers
* `clusters.pk`: serialized Python object containing a mapping of cluster numbers to a list of movie titles and IDs
* `recommend.py`: retrieve recommendations for a movie from the serialized cluster data
* `README.md`: this file

RECOMMENDATION USAGE
====================

* As a standalone program:
```sh
# get recommendations for a movie with specified MOVIE_TITLE
python3 recommend.py MOVIE_TITLE

# get recommendations for a randomly-selected movie
python3 recommend.py
```

* Or within a client program:
```python
import recommend
MOVIE_TITLE = 'Shanghai Noon'
res = recommend.recommend(MOVIE_TITLE)
print(res)
```

* Recommendations are returned as a JSON object in the following format:
```python
{
	'movie_queried': string,
	'cluster_number': integer,
	'num_movies': integer,
	'cluster_movies': [
		{
			'title': string,
			'id': string
		},
		{
			'title': string,
			'id': string
		},
		...
	]
}
```

* Example error response for a non-existent movie:
```python
{
	'Unknown movie': 'non-existent movie'
}
```
