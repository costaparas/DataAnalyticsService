#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Written by Saffat Akanda in October 2018
#Group movies into recommendation groups using clustering

import numpy as np
from sklearn.cluster import KMeans, MeanShift, AgglomerativeClustering, Birch
from sklearn.feature_extraction.text import CountVectorizer
import sys, json, codecs, re, collections, random, pickle, enum, sklearn.metrics


@enum.unique
class Model_Types(enum.Enum):
    KMEANS = 1
    MEANSHIFT = 2
    BIRCH = 3
    AGGLOMERATIVE = 4
    AGGLOMERATIVE_EUCLID = 5
    AGGLOMERATIVE_L1 = 6
    AGGLOMERATIVE_L2 = 7
    AGGLOMERATIVE_MAN = 8

debug = False
save_clusters = True
write_evaluation_metrics = False


def main():
    model_type, n_clusters, linkage = parse_args()

    # read movie data
    all_movies = read_movie_file()
    movies, n_movies = get_movies_dict(all_movies)

    # extract only relevant movie data
    genres = []
    directors = []
    actors = []
    embedded_plot_summary = []
    for movie in movies:
        genres.append(movies[movie]['Genre'])
        directors.append(movies[movie]['Director'])
        actors.append(movies[movie]['Actors'])
        embedded_plot_summary.append(movies[movie]['Plot'])

    if debug: print('Vectorizing')
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
        # Meanshift does not take in a number of clusters
        model = MeanShift(n_jobs=-1).fit_predict(cluster_features)
        n_clusters = len(set(model))
    elif model_type == Model_Types.BIRCH:
        model = Birch(n_clusters=n_clusters).fit_predict(cluster_features)
    elif model_type == Model_Types.AGGLOMERATIVE:
        model = AgglomerativeClustering(n_clusters=n_clusters,
                                        affinity="cosine", linkage=linkage).fit_predict(cluster_features)

    elif model_type == Model_Types.AGGLOMERATIVE_L1:
        model = AgglomerativeClustering(n_clusters=n_clusters,
                                        affinity="l1", linkage=linkage).fit_predict(cluster_features)

    elif model_type == Model_Types.AGGLOMERATIVE_L2:
        model = AgglomerativeClustering(n_clusters=n_clusters,
                                        affinity="l2", linkage=linkage).fit_predict(cluster_features)
    elif model_type == Model_Types.AGGLOMERATIVE_MAN:
        model = AgglomerativeClustering(n_clusters=n_clusters,
                                        affinity="manhattan", linkage=linkage).fit_predict(cluster_features)
    elif model_type == Model_Types.AGGLOMERATIVE_EUCLID:
        model = AgglomerativeClustering(n_clusters=n_clusters).fit_predict(cluster_features)

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
    if save_clusters: write_clusters(clusters, cluster_numbers)

    # Write out evaluation metrics
    if write_evaluation_metrics: write_metrics(model_type.name, cluster_features, model, linkage, n_clusters)

def parse_args():
    # too hard with argparse, so old-fashioned manual parsing
    if len(sys.argv) < 2:
        print('Usage: %s MODEL [N_CLUSTERS] [LINKAGE]' %sys.argv[0], file=sys.stderr)
        sys.exit(1)
    model_type = ''
    n_clusters = 0
    linkage = ''

    # choose ml model
    found_model = False
    for m in list(Model_Types):
       model = str(m)[str(m).index('.')+1:]
       if model == sys.argv[1]:
           model_type = m
           found_model = True
           break

    if not found_model:
        print('%s: invalid model type' %sys.argv[0], file=sys.stderr)
        sys.exit(1)
    if sys.argv[1] == 'MEANSHIFT' and len(sys.argv) > 2:
        print('%s: unexpected trailing arguments' %sys.argv[0], file=sys.stderr)
        sys.exit(1)
    if sys.argv[1] != 'MEANSHIFT' and len(sys.argv) < 3:
        print('%s: expecting number of clusters' %sys.argv[0], file=sys.stderr)
        sys.exit(1)
    elif sys.argv[1] != 'MEANSHIFT':
        try:
            n_clusters = int(sys.argv[2])
        except ValueError:
            print('%s: expecting integer number of clusters' %sys.argv[0], file=sys.stderr)
            sys.exit(1)
    if sys.argv[1].startswith('AGGLOMERATIVE') and len(sys.argv) < 4:
        print('%s: expecting linkage type' %sys.argv[0], file=sys.stderr)
        sys.exit(1)
    elif sys.argv[1].startswith('AGGLOMERATIVE'):
        if sys.argv[3] in ['average', 'complete']:
            linkage = sys.argv[3]
        else:
            print('%s: invalid linkage type' %sys.argv[0], file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) > 3:
        print('%s: unexpected trailing arguments' %sys.argv[0], file=sys.stderr)
        sys.exit(1)
    return model_type, n_clusters, linkage


def read_movie_file():
    try:
        with open('../data/movies-large.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (PermissionError, OSError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def get_movies_dict(all_movies, n_movies=1000):
    """
    # use a random subset of movies
    # keys = random.sample(list(all_movies), n_movies)
    keys = list(all_movies)
    movies = {}
    for key in keys:
        movies[key] = all_movies[key]

    return movies, len(keys)
    """
    return all_movies, len(list(all_movies))


# split data into tokens delimited by commas
def split(data):
    return re.split(r'\s*,\s*', data)


def write_clusters(clusters, cluster_numbers):
    if debug: print('Writing Clusters')
    try:
        with open('clusters.pk', 'wb') as f:
            pickle.dump(clusters, f)
        with open('cluster-numbers.pk', 'wb') as f:
            pickle.dump(cluster_numbers, f)
    except (PermissionError, OSError) as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


def write_metrics(model_name, model, labels, linkage, clusters=0, width=35, cwidth=20):

    # Write evaluation metrics to a file, while preserving stats of other models
    # We also preserve stats of the same model if it uses a different number of clusters
    try:
        with open('metrics.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
    except FileNotFoundError:
        with open('metrics.txt', 'w', encoding='utf-8') as f:
            data = ["{:<{width}} {:<{cwidth}} {:<{width}} {:<{width}}\n".format("Model Name", "# Clusters",
                                                                             "Silhouette Score", "Calinski-Hara Score",
                                                                             width=width, cwidth=cwidth)]
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

    if linkage != '':
        model_name += ' (' + linkage + ')'

    if line_to_write == len(data):
        data.append("{:<{width}} {:<{cwidth}} {:<{width}} {:<{width}}\n".format(
                model_name, clusters, silhouette_score, calinski_hara_score, width=width, cwidth=cwidth))
    else:
        data[line_to_write] = "{:<{width}} {:<{cwidth}} {:<{width}} {:<{width}}\n".format(
                model_name, clusters, silhouette_score, calinski_hara_score, width=width, cwidth=cwidth)

    with open('metrics.txt', 'w', encoding='utf-8') as f:
        f.writelines(data)


if __name__ == '__main__':
    main()
