#!/usr/bin/python3
#Written by Costa Paraskevopoulos in October 2018
#Plot overlayed scatter chart of clustering algorithm metrics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
	#read csv file into pandas dataframe
	df = pd.read_csv('metrics.csv')

	#rename columns
	df.columns = ['model', 'clusters', 'silhouette', 'callinski-hara']

	#get distinct models and number of clusters
	model_names = np.unique(list(df['model']))
	num_clusters = np.unique(list(df['clusters']))[1:]

	fig, ax = plt.subplots()
	colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet',
		'pink', 'brown', 'cyan', 'lime', 'silver', 'olive', 'magenta']

	#plot combined scatter plot
	i = 1
	chart_title = 'Silhouette Score vs Callinski-Hara Score'
	for model_name in model_names:
		model = df.query('model == "%s"' %model_name)
		ax = model.plot.scatter(x='silhouette', y='callinski-hara', ax=ax,
		c=colors[i], label=model_name, title=chart_title)
		i += 1

		#annotate plot with the number of clusters
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

	plt.show()

if __name__ == '__main__':
	main()
