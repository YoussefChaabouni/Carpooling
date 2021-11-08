#!/bin/python3

#This file is used to created a graph from a file in the results


import matplotlib.pyplot as plt

List_nb_drivers = [i for i in range(10,1000,20)] ## Needs to be changed
List_proportion_served = []

with open('Results/result_graph_test1.txt', 'r') as file:
    l = file.readlines()

lines = []
for line in l:
    line = line[1:-2]
    line = line.split(',')
    line = [float(line[i]) for i in range(len(line))]
    lines.append(line)

for i in range(len(lines[0])):
    List_proportion_served.append( sum([lines[k][i] for k in range(len(lines))]) / len(lines) )


plt.plot(List_nb_drivers,List_proportion_served)
plt.xlabel('nb drivers')
plt.ylabel('riders served')
plt.show()
