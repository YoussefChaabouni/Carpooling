'''
This file should primarily deal with relevant statistics 
'''

from typing import List
from PersonClasses import Driver, Rider
import matplotlib.pyplot as plt
import numpy as np


#from new_code.CSV_creation import NUMBER_OF_RIDERS


# Vehicle max capacity
def vehicle_maximum_occupancy(DRIVERS : List[Driver],system : str,save_path):

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
    plt.title(title,fontsize = 18)
    #plt.show()
    if save_path != "" :
        plt.savefig(save_path+"/Vehicle Maximum Occupancy in "+system+" System.png")    
    plt.show()
    return 0

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
    labels = ['UNSERVED', 'FOOT',
        'TRANSIT','CARPOOLING', 'INTEGRATED']

    data = [no_solution*100, foot*100, transit*100,carpooling*100,integrated*100]


    explode = (0, 0, 0, 0, 0) 

    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.pie(data, explode=explode,labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(loc="upper right")
    plt.title("Integrated system",fontsize = 18)

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
    labels = ['UNSERVED', 'FOOT',
        'TRANSIT','CARPOOLING']

    data = [no_solution*100, foot*100, transit*100,carpooling*100]


    explode = (0, 0, 0, 0) 

    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()

    plt.title("Current system",fontsize = 18)

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
    labels = [ 'UNSERVED', 'FOOT',
        'TRANSIT']

    data = [ no_solution*100, foot*100, transit*100]


    explode = ( 0, 0, 0) 

    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.pie(data, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()

    plt.title("No Carpooling System",fontsize = 18)
	#if save_path != "":
	#	plt.savefig(save_path+"system comparison.png",format='png')

    plt.show()
def boarding_alighting_statistics(all_riders,save_path):
    total_relative_mounts = [0,0,0,0,0,0,0,0]
    total_relative_dismounts = [0,0,0,0,0,0,0,0]
    total = 0
    for r in all_riders[2]:
        if r.solution == "integrated":
            total +=1
        for i in range(len(r.relative_boarding)):
            total_relative_mounts[i] += r.relative_boarding[i]
            total_relative_dismounts[i] += r.relative_alighting[i]
    
    percentage_mounts = np.array(total_relative_mounts) * 100/np.sum(total_relative_mounts)
    percentage_dismounts = np.array(total_relative_dismounts) * 100/np.sum(total_relative_dismounts)

    
    ## plot 
    labels = ["org","MPorg","Mprime","Sorg","Sdst","Mseconde","MPdst","dst"]

    data_mount = percentage_mounts 

    data_dismount = percentage_dismounts


    explode = ( 0, 0, 0, 0,0,0,0,0) 

    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.pie(data_mount, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()

    plt.title("Relative boarding frequency percentage",fontsize = 18)

    if save_path != "":
        plt.savefig(save_path+"/mounting.png",format='png')
	#if save_path != "":
	#	plt.savefig(save_path+"system comparison.png",format='png')

    plt.show()

    fig1, ax1 = plt.subplots(figsize=(9, 6))
    ax1.pie(data_dismount, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()

    plt.title("Relative alighting frequency percentage",fontsize = 18)
	#if save_path != "":
	#	plt.savefig(save_path+"system comparison.png",format='png')

    if save_path != "":
        plt.savefig(save_path+"/dismounting.png",format='png')

    plt.show()

def better_camembert(all_solutions,save_path):
        # import necessary libraries
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    carpooling_i = 0
    foot_i = 0
    transit_i = 0
    no_solution_i = 0
    integrated = 0

    for solution in all_solutions[2]:
        if solution == "carpooling":
            carpooling_i +=1
        if solution == "transit":
            transit_i += 1
        if solution == "foot":
            foot_i += 1
        if solution == "no solution":
            no_solution_i +=1
        if solution == "integrated":
            integrated +=1
        
    
    carpooling_cs = 0
    foot_cs = 0
    transit_cs = 0
    no_solution_cs = 0
    

    for solution in all_solutions[1]:
        if solution == "carpooling":
            carpooling_cs +=1
        if solution == "transit":
            transit_cs += 1
        if solution == "foot":
            foot_cs += 1
        if solution == "no solution":
            no_solution_cs +=1
    
   
    foot_nc = 0
    transit_nc = 0
    no_solution_nc = 0
    

    for solution in all_solutions[0]:

        if solution == "transit":
            transit_nc += 1
        if solution == "foot":
            foot_nc += 1
        if solution == "no solution":
            no_solution_nc +=1

    NUMBER_OF_RIDERS = len(all_solutions[0])
    # create DataFrame
    df = pd.DataFrame({'integrated' : [integrated*100/NUMBER_OF_RIDERS,0,0,0],
                    'foot': [foot_i*100/NUMBER_OF_RIDERS,foot_cs*100/NUMBER_OF_RIDERS,foot_nc*100/NUMBER_OF_RIDERS,0],
                    'transit': [transit_i*100/NUMBER_OF_RIDERS,transit_cs*100/NUMBER_OF_RIDERS,transit_nc*100/NUMBER_OF_RIDERS,0],
                    'carpooling':[carpooling_i*100/NUMBER_OF_RIDERS,carpooling_cs*100/NUMBER_OF_RIDERS,0,0],
                    
                    'unserved': [no_solution_i*100/NUMBER_OF_RIDERS,no_solution_cs*100/NUMBER_OF_RIDERS,no_solution_nc*100/NUMBER_OF_RIDERS,0]},
                    index=['Integrated', 'Current','No Carpooling',''])
    
    
    # create stacked bar chart for monthly temperatures
    
    plot = df.plot(kind='bar', stacked=True, color=['red', 'blue', 'green','yellow','gray'])
    plt.ylabel('Percentage of riders')#.legend(loc="lower_left")
    
    # labels for x & y axis
    #plt.xlabel('System')
    #plt.ylabel('Percentage of riders')
    
    if save_path != "":
        plt.savefig(save_path+"/served and unserved.png",format='png')


    plt.show()
    # title of plot
    #plt.title('')
    #return plot

def better_waiting_walking_times(ALL_RIDERS,save_path):
    average_walking_i = 0
    average_waiting_i = 0 

    average_walking_c = 0
    average_waiting_c = 0 

    average_walking_nc = 0
    average_waiting_nc = 0 
    relevant_rider_counter_i = 0 #don't count not served riders
    for rider in ALL_RIDERS[2] :
        if rider.waiting_time != np.Infinity and rider.born_time<60:
            average_walking_i += rider.walking_distance*5
            average_waiting_i += rider.waiting_time
            relevant_rider_counter_i +=1
    
    average_walking_i =(average_walking_i)/ relevant_rider_counter_i
    average_waiting_i /= relevant_rider_counter_i

    relevant_rider_counter_c = 0 #don't count not served riders
    for rider in ALL_RIDERS[1] :
        if rider.waiting_time != np.Infinity and rider.born_time<60:
            average_walking_c += rider.walking_distance*5
            average_waiting_c += rider.waiting_time
            relevant_rider_counter_c +=1
    
    average_walking_c =(average_walking_c)/ relevant_rider_counter_c
    average_waiting_c /= relevant_rider_counter_c

    relevant_rider_counter_nc = 0 #don't count not served riders
    for rider in ALL_RIDERS[0] :
        if rider.waiting_time != np.Infinity and rider.born_time<60:
            average_walking_nc += rider.walking_distance*5
            average_waiting_nc += rider.waiting_time
            relevant_rider_counter_nc +=1
    
    average_walking_nc =(average_walking_nc)/ relevant_rider_counter_nc
    average_waiting_nc /= relevant_rider_counter_nc
    import pandas as pd
    import seaborn as sns
    df = pd.DataFrame({"Time":["Walking Time","Waiting Time","Walking Time","Waiting Time","Walking Time","Waiting Time","Walking Time","Waiting Time"],
                        "Time (Minutes)":[average_walking_i,average_waiting_i,average_walking_c,average_waiting_c,average_walking_nc,average_waiting_nc,0,0],
                        "System":["Integrated","Integrated","Current","Current","No Carpooling","No Carpooling","",""]})
    plot = sns.barplot(x="System",y="Time (Minutes)",hue="Time",data = df)
    
    if save_path != "":
        plt.savefig(save_path+"/waiting and walking times.png",format='png')


    plt.show()

    return plot