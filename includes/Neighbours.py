#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:10:25 2020

@author: ari
"""

# Example of getting neighbors for an instance
from math import sqrt

# calculate the Euclidean distance between two vectors
def euclidean_distance(row1, row2): # TODO : change the function
	distance = 0.0
	for i in range(len(row1)-1):
		distance += (row1[i] - row2[i])**2
	return sqrt(distance)

# Locate the most similar neighbors
def get_neighbors(trains, wantedTrain, num_neighbors):
	distances = list()
	for train_row in trains:
		dist = euclidean_distance(wantedTrain, train_row)
		distances.append((train_row, dist))
	distances.sort(key=lambda tup: tup[1])
	neighbors = list()
	for i in range(num_neighbors):
		neighbors.append(distances[i][0])
	return neighbors

# Test distance function
#dataset = [[2.7810836,2.550537003,0],
	#[1.465489372,2.362125076,0],
	#[3.396561688,4.400293529,0],
	#[1.38807019,1.850220317,0],
	#[3.06407232,3.005305973,0],
	#[7.627531214,2.759262235,1],
	#[5.332441248,2.088626775,1],
	#[6.922596716,1.77106367,1],
	#[8.675418651,-0.242068655,1],
	#[7.673756466,3.508563011,1]]
#neighbors = get_neighbors(dataset, dataset[0], 3)
#for neighbor in neighbors:
#	print(neighbor)
