from typing import List
from pydantic import ListMaxLengthError
from PersonClasses import Driver, Rider
import pickle
import numpy as np


from meansClasses import Foot, Train
# get the data and turn it into a dataframe


# read the pickle variables
# read the data files

with open('experiments/0.08/data/riders.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    riders_list = pickle.load(f)

# read the data files
with open('experiments/0.08/data/drivers.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    drivers_list = pickle.load(f)
    
with open('experiments/0.08/data/graphs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    graphs_list = pickle.load(f)

# will contain columns with name, type, x_coord, y_coord, time, means
data_list = []
G = graphs_list[0]
#print(riders_list[0])
# add riders to dataframe
size = 1000
for rider in riders_list[2]:
           
    trajectory = rider.get_trajectory()
    size += 100
    times_list = [i for i in range(180)]
    arrival_times = [int(x) for x in trajectory.arr_time_list]
    index = 0
    intermediate_x = [G.get_node(rider.pos_depart).x_coordinate]
    intermediate_y = [G.get_node(rider.pos_depart).y_coordinate]
    means = "None"
    solution = rider.solution
    if solution != "no solution":
        solution = "served"
    else:
        solution = "unserved"

    # modify initial arrival time so that it fits waiting at home before going out
    if len(arrival_times) >= 2:
        arrival_times[0] = int(arrival_times[1] - G.get_distance(G.get_node(rider.pos_depart),G.get_node(trajectory.node_id_list[1]))/(rider.walking_speed/60))
    for t in times_list :

        # if t is an arrival time

        if t in range(len(arrival_times)-1):


            # origin node
            x_org = G.get_node(trajectory.node_id_list[index]).x_coordinate
            y_org = G.get_node(trajectory.node_id_list[index]).y_coordinate

            # final node
            x_dest = G.get_node(trajectory.node_id_list[index+1]).x_coordinate
            y_dest = G.get_node(trajectory.node_id_list[index+1]).y_coordinate

            means = trajectory.means_list[index+1]

            if isinstance(means,Foot):
                means = "Foot"
            if isinstance(means,Driver):
                means = "Carpool"
            if isinstance(means,Train):
                means = "Train"

            # getting intermediate positions for every minute that passes
            intervals = [arrival_times[t]+x*(arrival_times[t+1]-arrival_times[t])/int(arrival_times[t+1]-arrival_times[t]) for x in range(int(arrival_times[t+1]-arrival_times[t]))] # every minute
            #for i in range(len(intervals)):
            intermediate_x = [x_org + i*(x_dest-x_org)/np.abs(arrival_times[t+1]-arrival_times[t]) for i in range(int(arrival_times[t+1]-arrival_times[t]))]
            intermediate_y = [y_org + i*(y_dest-y_org)/np.abs(arrival_times[t+1]-arrival_times[t]) for i in range(int(arrival_times[t+1]-arrival_times[t]))]

                #intermediate_x.append[x_org+]
            if solution != "no solution":
                rider_type = rider.solution
            else:
                rider_type = "unserved rider"
            for i in range(len(intervals)):
                data_list.append([rider.id,
                "served rider",
                intermediate_x[i],
                intermediate_y[i],
                intervals[i],
                means,
                rider_type
                ])

            index +=1
        '''else :
            data_list.append([rider.id,
            "rider",
            intermediate_x[-1],
            intermediate_y[-1],
            t,
            means
            ])'''
        
print(len(data_list))
L = []
for i in range(len(data_list)):
    if data_list[i][0] == "R206":
        L.append(data_list[i])

#print(L)

for rider in riders_list[2]:
    if rider.id == "R588":
        trajectory = rider.get_trajectory()
        print("node list of R206 = ",rider.id," ",trajectory.node_id_list)
        print("arrival times of R206 = ",rider.id," ",trajectory.arr_time_list)
        print("departure times of R206 = ",rider.id," ",trajectory.dep_time_list)
        print("means of R206 = ",rider.id," ",[x.id for x in trajectory.means_list])
        print("solution = ",rider.solution)

# add nodes

for node in G.node_list:
    solution="node"
    if node.id[0] == "M":
        for t in range(180):
            data_list.append([node.id,
            "meeting point",
            node.x_coordinate,
            node.y_coordinate,
            t,
            "node",
            "node"])
    if node.id[0] == "S":
        for t in range(180):
            data_list.append([node.id,
            "station",
            node.x_coordinate,
            node.y_coordinate,
            t,
            "node",
            "node"])

# drivers
for d in drivers_list[2]:
           
    trajectory = d.get_trajectory()
    size += 100
    times_list = [i for i in range(180)]
    arrival_times = [int(x) for x in trajectory.arr_time_list]
    index = 0
    intermediate_x = [G.get_node(d.pos_depart).x_coordinate]
    intermediate_y = [G.get_node(d.pos_depart).y_coordinate]
    means = "Drive"
    solution = "drive"

    # modify initial arrival time so that it fits waiting at home before going out
   # if len(arrival_times) >= 2:
    #    arrival_times[0] = int(arrival_times[1] - G.get_distance(G.get_node(rider.pos_depart),G.get_node(trajectory.node_id_list[1]))/(rider.walking_speed/60))
    for t in times_list :

        # if t is an arrival time

        if t in range(len(arrival_times)-1):


            # origin node
            x_org = G.get_node(trajectory.node_id_list[index]).x_coordinate
            y_org = G.get_node(trajectory.node_id_list[index]).y_coordinate

            # final node
            x_dest = G.get_node(trajectory.node_id_list[index+1]).x_coordinate
            y_dest = G.get_node(trajectory.node_id_list[index+1]).y_coordinate


            # getting intermediate positions for every minute that passes
            intervals = [arrival_times[t]+x*(arrival_times[t+1]-arrival_times[t])/int(arrival_times[t+1]-arrival_times[t]) for x in range(int(arrival_times[t+1]-arrival_times[t]))] # every minute
            #for i in range(len(intervals)):
            intermediate_x = [x_org + i*(x_dest-x_org)/np.abs(arrival_times[t+1]-arrival_times[t]) for i in range(int(arrival_times[t+1]-arrival_times[t]))]
            intermediate_y = [y_org + i*(y_dest-y_org)/np.abs(arrival_times[t+1]-arrival_times[t]) for i in range(int(arrival_times[t+1]-arrival_times[t]))]

                #intermediate_x.append[x_org+]
            for i in range(len(intervals)):
                data_list.append([d.id,
                "driver",
                intermediate_x[i],
                intermediate_y[i],
                intervals[i],
                means,
                solution
                ])

            index +=1

import pandas as pd
df = pd.DataFrame(data_list, columns =['name', 'type', 'x_coord', 'y_coord', 'time', 'means','served'])

print(df.head(20))
df.to_csv("Generate_Data/animationRidersDrivers008.csv")


'''
for driver in drivers_list :
    trajectory = driver.journey
    times_list = [i for i in range(180)]
    arrival_times = [int(x) for x in trajectory.arrival_times]
    index = 0
    for t in times_list :
'''

def get_user_trajectory(user,data_list):
    trajectory = user.get_trajectory()
    size += 100
    times_list = [i for i in range(180)]
    arrival_times = [int(x) for x in trajectory.arr_time_list]
    index = 0
    intermediate_x = [G.get_node(user.pos_depart).x_coordinate]
    intermediate_y = [G.get_node(user.pos_depart).y_coordinate]
    means = "None"
    for t in times_list :

        # if t is an arrival time

        if t in range(len(arrival_times)-1):

            # origin node
            x_org = G.get_node(trajectory.node_id_list[index]).x_coordinate
            y_org = G.get_node(trajectory.node_id_list[index]).y_coordinate

            # final node
            x_dest = G.get_node(trajectory.node_id_list[index+1]).x_coordinate
            y_dest = G.get_node(trajectory.node_id_list[index+1]).y_coordinate

            means = trajectory.means_list[index+1]

            if isinstance(means,Foot):
                means = "Foot"
            if isinstance(means,Driver):
                means = "Carpool"
            if isinstance(means,Train):
                means = "Train"

            # getting intermediate positions for every minute that passes
            intervals = [arrival_times[t]+x*(arrival_times[t+1]-arrival_times[t])/int(arrival_times[t+1]-arrival_times[t]) for x in range(int(arrival_times[t+1]-arrival_times[t]))] # every minute
            #for i in range(len(intervals)):
            intermediate_x = [x_org + i*(x_dest-x_org)/np.abs(arrival_times[t+1]-arrival_times[t]) for i in range(int(arrival_times[t+1]-arrival_times[t]))]
            intermediate_y = [y_org + i*(y_dest-y_org)/np.abs(arrival_times[t+1]-arrival_times[t]) for i in range(int(arrival_times[t+1]-arrival_times[t]))]

                #intermediate_x.append[x_org+]
            for i in range(len(intervals)):
                data_list.append([rider.id,
                "rider",
                intermediate_x[i],
                intermediate_y[i],
                intervals[i],
                means
                ])

            index +=1

