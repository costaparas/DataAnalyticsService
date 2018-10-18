#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Plot overlayed scatter chart of clustering algorithm metrics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('metrics.csv')
	df.columns = ['model', 'clusters', 'silhouette', 'callinski-hara']
	colors = ['red', 'orange', 'yellow', 'green', 'blue',
		'indigo', 'violet', 'pink']
	model_names = ['KMEANS', 'MEANSHIFT', 'BIRCH']
#TODO: negative scale
#	model_names = ['KMEANS', 'MEANSHIFT', 'BIRCH',
#		'AGGLOMERATIVE', 'AGGLOMERATIVE_EUCLID', 'AGGLOMERATIVE_L1',
#		'AGGLOMERATIVE_L2', 'AGGLOMERATIVE_MAN']

	fig, ax = plt.subplots()

	num_clusters = np.unique(list(df['clusters']))[1:]

	#plot combined scatter plot
	i = 1
	for model_name in model_names:
		model = df.query('model == "%s"' %model_name)
		ax = model.plot.scatter(x='silhouette',
			y='callinski-hara', ax=ax, c=colors[i], label=model_name, title='Silhouette Score vs Callinksi-Hara Score')

		#annotate with the number of clusters
		x = list(model['silhouette'])
		y = list(model['callinski-hara'])
		if model_name == 'MEANSHIFT':
			n_clusters = [list(model['clusters'])[0]]
		else:
			n_clusters = num_clusters
		j = 0
		for label in n_clusters:
			ax.annotate(label, (x[j], y[j]))
			j += 1

		i += 1

	plt.show()

if __name__ == '__main__':
	main()
