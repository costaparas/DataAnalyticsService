import numpy as np
from sklearn.cluster import KMeans, MeanShift
from sklearn.feature_extraction.text import CountVectorizer
import sys, json, codecs, re, collections, random, pickle, sklearn.metrics, enum


@enum.unique
class Model_Types(enum.Enum):
    KMEANS = 1
    MEANSHIFT = 2

debug = True
write_evaluation_metrics = True
model_type = Model_Types.KMEANS


def read_movie_file():
    try:
        with open('../data/movies-full.json', 'r', encoding="utf-8") as f:
            return json.load(f)
    except (PermissionError, OSError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def get_movies_dict(all_movies, n_movies):
    #keys = random.sample(list(all_movies), n_movies)
    keys = list(all_movies)
    movies = {}
    for key in keys:
        movies[key] = all_movies[key]

    return movies


def write_clusters(clusters, cluster_numbers):
    if debug: print("Writing Clusters")
    try:
        with open('clusters.pk', 'wb') as f:
            pickle.dump(clusters, f)
        with open('cluster-numbers.pk', 'wb') as f:
            pickle.dump(cluster_numbers, f)
    except (PermissionError, OSError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def write_metrics(model_name, model, labels, clusters=0, width=30):
    # Write evaluation metrics to a file, while preserving stats of other models
    # We also preserve stats of the same model if it uses a different number of clusters
    try:
        with open('mlMetrics.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
    except FileNotFoundError:
        with open('mlMetrics.txt', 'w', encoding='utf-8') as f:
            data = ["{:{width}} {:{width}} {:{width}} {:{width}}\n".format("Model Name", "# Clusters",
                                                                             "Silhouette Score", "Calinski-Hara Score",
                                                                             width=width)]
            f.write(data[0])


    line_to_write = len(data)
    for count, line in enumerate(data):
        lline = line.split()
        if lline[0] == model_name and lline[1] == str(clusters):
            line_to_write = count
            break

    # These are heuristics to tell us how "good" our clustering is, how similar things in the cluster are
    # We want to maximise these without getting our clusters so high that they become too small
    silhouette_score = sklearn.metrics.silhouette_score(model, labels)
    calinski_hara_score = sklearn.metrics.calinski_harabaz_score(model, labels)

    if line_to_write == len(data):
        data.append("{:{width}} {:{width}} {:{width}} {:{width}}\n".format(model_name, clusters, silhouette_score, calinski_hara_score, width=width))
    else:
        data[line_to_write] = "{:{width}} {:{width}} {:{width}} {:{width}}\n".format(
                model_name, clusters, silhouette_score, calinski_hara_score, width=width)

    with open('mlMetrics.txt', 'w', encoding='utf-8') as f:
        f.writelines(data)


def main():
    # read movie data
    all_movies = read_movie_file()

    # KMeans will run out of memory on full dataset
    n_movies = 1000
    #n_movies =
    n_clusters = int(n_movies / 10)
    #n_clusters = 200

    movies = get_movies_dict(all_movies, n_movies)

    # extract only relevant movie data
    genres = []
    directors = []
    actors = []
    embedded_plot_summary = []
    for movie in movies:
        genres.append(movies[movie]['Genre'])
        directors.append(movies[movie]['Director'])
        actors.append(movies[movie]['Actors'])
        embedded_plot_summary.append(movies[movie]["Plot"])

    if debug: print("Vectorizing")
    genre_vectorizer = CountVectorizer(tokenizer=split, max_features=100)
    genres_vectorized = genre_vectorizer.fit_transform(genres)
    # print(genre_vectorizer.get_feature_names())

    director_vectorizer = CountVectorizer(tokenizer=split, max_features=100)
    directors_vectorized = director_vectorizer.fit_transform(directors)
    # print(director_vectorizer.get_feature_names())

    actor_vectorizer = CountVectorizer(tokenizer=split, max_features=100)
    actors_vectorized = actor_vectorizer.fit_transform(actors)
    # print(actor_vectorizer.get_feature_names())

    plot_vectorizer = CountVectorizer(tokenizer=split, max_features=100)
    plot_vectorized = plot_vectorizer.fit_transform(embedded_plot_summary)
    # print(plot_vectorizer.get_feature_names())

    cluster_features = np.hstack([
        genres_vectorized.todense(),
        directors_vectorized.todense(),
        actors_vectorized.todense(),
        plot_vectorized.todense()
    ])

    # If a Clustering algorithm supports verbose, add it as a debug option
    if model_type == Model_Types.KMEANS:
        # -1 jobs, means use all available cores
        if debug: model = KMeans(n_clusters=n_clusters, verbose=1, n_jobs=-1).fit_predict(cluster_features)
        else: model = KMeans(n_clusters=n_clusters, n_jobs=-1).fit_predict(cluster_features)

    elif model_type == Model_Types.MEANSHIFT:
        model = MeanShift(n_jobs=-1).fit_predict(cluster_features)
        n_clusters = len(set(model))


    # group movies into clusters, along with their title and ID
    clusters = collections.defaultdict(list)
    cluster_numbers = {}
    i = 0
    for movie in movies:
        title = movies[movie]['Title']
        cluster_numbers[title] = model[i]
        clusters[model[i]].append({'title': title, 'id': movie})
        i += 1

    # serialize cluster data for future retrieval
    write_clusters(clusters, cluster_numbers)

    # Write out evaluation metrics
    if write_evaluation_metrics: write_metrics(model_type.name, cluster_features, model, n_clusters)


# split data into tokens delimited by commas
def split(data):
    return re.split(r'\s*,\s*', data)


if __name__ == '__main__':
    main()
