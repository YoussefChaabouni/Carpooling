'''
This file should primarily deal with relevant statistics 
'''

from typing import List
from PersonClasses import Driver, Rider
import matplotlib.pyplot as plt
import numpy as np

#from new_code.CSV_creation import NUMBER_OF_RIDERS


# Vehicle max capacity
def vehicle_maximum_occupancy(DRIVERS : List[Driver],system : str):

    max_list = [0,0,0,0,0]
    for d in DRIVERS:
        current_capacity_list = d.get_current_capacity()
        
        max_current_capacity = get_maximum(current_capacity_list)
        if max_current_capacity in range(0,5):
            max_list[max_current_capacity] += 1
        else :
            print("this capacity is weird, it's = ",max_current_capacity)
            print("the driver responsible for this is ",d.get_id())
            print("his current capacity list is = ",current_capacity_list)
    # we should plot this one here
    labels = ['0 rider', '1 rider',
        '2 riders','3 riders', '4 riders']

    data = [item*100/len(DRIVERS) for item in max_list]


    explode = (0, 0, 0, 0, 0) 

    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()
    title = "Vehicle Maximum Occupancy in "+system+" System"
    plt.title(title)
    plt.show()
    return max_list

# average waiting and walking time
def average_walking_and_waiting_time(RIDERS : List[Rider],system : str):
    average_walking = 0
    average_waiting = 0 
    relevant_rider_counter = 0 #don't count not served riders
    for rider in RIDERS :
        if rider.waiting_time != np.Infinity:
            average_walking += rider.walking_distance
            average_waiting += rider.waiting_time
            relevant_rider_counter +=1
    
    average_walking /= relevant_rider_counter
    average_waiting /= relevant_rider_counter
    data = [average_walking,average_waiting]
    X = np.arange(1)
    fig = plt.figure()
    
    ax = fig.add_axes([0,0,1,1])
   
    ax.set_yticks(np.arange(0,30,1))
    ax.bar(X + 0.00, data[0], color = 'b', width = 0.1)
    ax.bar(X + 0.25, data[1], color = 'r', width = 0.1)
    ax.legend(labels=["average walking distance","average waiting time"])
    title = "Average waiting time and walking distance in "+system+" system"
    ax.set_title(title)
    plt.show()

    return average_walking, average_waiting
 

# helper function to get the maximum capacity
def get_maximum(current_capacity):
    min = 4
    for i in range(len(current_capacity)):
        if current_capacity[i] < min :
            min = current_capacity[i]
    return 4 - min

def camembert_function(all_solutions):

##___________________INTEGRATED_________________________
    carpooling = 0
    foot = 0
    transit = 0
    no_solution = 0
    integrated = 0

    for solution in all_solutions[2]:
        if solution == "carpooling":
            carpooling +=1
        if solution == "transit":
            transit += 1
        if solution == "foot":
            foot += 1
        if solution == "no solution":
            no_solution +=1
        if solution == "integrated":
            integrated +=1
    
    NUMBER_OF_RIDERS = len(all_solutions[2])

    carpooling = carpooling / NUMBER_OF_RIDERS
    foot = foot / NUMBER_OF_RIDERS
    transit = transit / NUMBER_OF_RIDERS
    no_solution = no_solution / NUMBER_OF_RIDERS
    integrated = integrated / NUMBER_OF_RIDERS

    ## plot 
    labels = ['NO SOLUTION', 'FOOT',
        'TRANSIT','CARPOOLING', 'INTEGRATED']

    data = [no_solution*100, foot*100, transit*100,carpooling*100,integrated*100]


    explode = (0, 0, 0, 0, 0) 

    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()
    plt.title("Integrated system")

    plt.show()

##___________________Current_________________________
    carpooling = 0
    foot = 0
    transit = 0
    no_solution = 0
    integrated = 0

    for solution in all_solutions[1]:
        if solution == "carpooling":
            carpooling +=1
        if solution == "transit":
            transit += 1
        if solution == "foot":
            foot += 1
        if solution == "no solution":
            no_solution +=1

    


    carpooling = carpooling / NUMBER_OF_RIDERS
    foot = foot / NUMBER_OF_RIDERS
    transit = transit / NUMBER_OF_RIDERS
    no_solution = no_solution / NUMBER_OF_RIDERS


    ## plot 
    labels = ['NO SOLUTION', 'FOOT',
        'TRANSIT','CARPOOLING']

    data = [no_solution*100, foot*100, transit*100,carpooling*100]


    explode = (0, 0, 0, 0) 

    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()

    plt.title("Current system")

    plt.show()

##___________________NO CARPOOLING_________________________

    foot = 0
    transit = 0
    no_solution = 0


    for solution in all_solutions[0]:

        if solution == "transit":
            transit += 1
        if solution == "foot":
            foot += 1
        if solution == "no solution":
            no_solution +=1

    foot = foot / NUMBER_OF_RIDERS
    transit = transit / NUMBER_OF_RIDERS
    no_solution = no_solution / NUMBER_OF_RIDERS


    ## plot 
    labels = [ 'NO SOLUTION', 'FOOT',
        'TRANSIT']

    data = [ no_solution*100, foot*100, transit*100]


    explode = ( 0, 0, 0) 

    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()

    plt.title("No Carpooling System")

    plt.show()