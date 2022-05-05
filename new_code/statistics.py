'''
This file should primarily deal with relevant statistics 
'''

from typing import List
from PersonClasses import Driver, Rider
import matplotlib.pyplot as plt
import numpy as np

from graphClasses import Graph


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
    
    if total_relative_mounts != [0,0,0,0,0,0,0,0] :
        percentage_mounts = np.array(total_relative_mounts) * 100/np.sum(total_relative_mounts)
    else:
        percentage_mounts = np.array([0,0,0,0,0,0,0,0])

    if total_relative_dismounts != [0,0,0,0,0,0,0,0] :

        percentage_dismounts = np.array(total_relative_dismounts) * 100/np.sum(total_relative_dismounts)
    else:
        percentage_dismounts = np.array([0,0,0,0,0,0,0,0])
    
    ## plot 
    labels = ["org","MPorg","Mprime","Sorg","Sdst","Mseconde","MPdst","dst"]

    print("percentage mounts = ",percentage_mounts)
    data_mount = percentage_mounts 

    data_dismount = percentage_dismounts


    explode = ( 0, 0, 0, 0,0,0,0,0) 

    print("data_mount = ",data_mount)

    if (data_mount != np.array([0,0,0,0,0,0,0,0])).any():
        fig1, ax1 = plt.subplots(figsize=(9, 6))
        ax1.pie(data_mount, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=0)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.legend()

        plt.title("Relative boarding frequency percentage",fontsize = 18)

        if save_path != "":
            plt.savefig(save_path+"/boarding.png",format='png')
        #if save_path != "":
        #	plt.savefig(save_path+"system comparison.png",format='png')

        plt.show()

    print("data_dismount = ",data_dismount)
    if (data_dismount != np.array([0,0,0,0,0,0,0,0])).any() :
        fig1, ax1 = plt.subplots(figsize=(9, 6))
        ax1.pie(data_dismount, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=0)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.legend()

        plt.title("Relative alighting frequency percentage",fontsize = 18)
        #if save_path != "":
        #	plt.savefig(save_path+"system comparison.png",format='png')

        if save_path != "":
            plt.savefig(save_path+"/alighting.png",format='png')

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

# function to calculate the distance between (MPorg - org) and (MPdst - dst) for all drivers
# the output is a histogram giving the percentage of points within 100m, 200m....1km
def distances_of_meeting_points(drivers_list: List[Driver],G: Graph,save_path):


    # origins
    distances_list = [0.3*int(x) for x in range(10)]
    distances_from_origin = [0]*10
    distances_from_destination = [0]*10


    for d in drivers_list:  
        
        org = G.get_node(d.pos_depart)
        dst = G.get_node(d.pos_arrivee)

        MPdst = G.get_closest_MP_or_Station(dst,"MPs")
        MPorg = G.get_closest_MP_or_Station(org,"MPs")
        
        distance_org = G.get_distance(org,MPorg)
        distance_dst = G.get_distance(dst,MPdst)
        for i in range(len(distances_list)):
            if distance_org <= distances_list[i]:
                distances_from_origin[i] += 1
                break
        
        for i in range(len(distances_list)):
            if distance_dst <= distances_list[i]:
                distances_from_destination[i] += 1
                break


            
    
    new_distances_org = [x*100/len(drivers_list) for x in distances_from_origin]
    new_distances_dst = [x*100/len(drivers_list) for x in distances_from_destination]
    import pandas as pd
    import seaborn as sns

    df = pd.DataFrame({"distance(per m)" :[int(x*1000) for x in distances_list],
    "percentage(%)" : new_distances_org})
    plot = sns.barplot(x="distance(per m)",y="percentage(%)",data = df)
    plt.title("Distances of closest meeting points from origins")

    if save_path != "":
        plt.savefig(save_path+"/Distance of closest MP from origin.png",format='png')

    plt.show()

    df = pd.DataFrame({"distance(per m)" :[int(x*1000) for x in distances_list],
    "percentage(%)" : new_distances_dst})
    plot = sns.barplot(x="distance(per m)",y="percentage(%)",data = df)
    plt.title("Distances of closest meeting points from destinations")

    if save_path != "":
        plt.savefig(save_path+"/Distance of closest MP from destination.png",format='png')


    plt.show()
    return distances_from_origin, distances_from_destination

def detour_percentage_per_driver(drivers_list: List[Driver],G: Graph,save_path):

    detours = []
    
    for d in drivers_list :

        trajectory = d.get_trajectory()
        nodes_list = trajectory.node_id_list
        detour_distance = 0

        org_d = G.get_node(d.pos_depart)	
        dst_d = G.get_node(d.pos_arrivee)
        m_org_d = G.get_closest_MP_or_Station(org_d,"MPs")
        m_dst_d = G.get_closest_MP_or_Station(dst_d,"MPs")
        no_detour_distance = G.get_distance(org_d,dst_d)

        weird_drivers = []
        if len(nodes_list)>2:
            for i in range(len(nodes_list)-1) :
                detour_distance += G.get_distance(G.get_node(nodes_list[i]),G.get_node(nodes_list[i+1]))

            if detour_distance != 0:
                detours.append(abs(int((detour_distance - no_detour_distance)*100/detour_distance)))
            else:
                weird_drivers.append(d)
                detours.append(0)
        else :
            detours.append(0)
        #print("_________________",d.id,"__________________")
        #print("no_detour_distance = ",no_detour_distance)
        #print("detour_distance = ",detour_distance)
        #print("trajectory = ",d.get_trajectory().node_id_list)
        if detour_distance != 0 :
            print((int((detour_distance - no_detour_distance)*100/detour_distance)))
    
    #print(detours)
    #print("number of drivers = ",len(drivers_list))
    max_detour = int(drivers_list[0].detour_rate*100)
    detours_counter = [0]*(max_detour+1)

    for item in detours :
        for i in range(len(detours_counter)):
            if item == i :
                detours_counter[i] += 1
                

    import pandas as pd
    import seaborn as sns

    df = pd.DataFrame({"detour(%)" :range(max_detour+1),
    "count" : detours_counter})
    plot = sns.barplot(x="detour(%)",y="count",data = df)
    plt.title("Number of detours taken by percentage of detour")

    if save_path != "":
        plt.savefig(save_path+"/Number of detours per percentage of detours.png",format='png')

    plt.show()

    return detours, detours_counter, weird_drivers 

def station_coverage_per_driver(drivers_list: List[Driver],G : Graph,save_path):

    resulting_list = []
    count_percentage = [0,0,0]
    for d in drivers_list:
        
        stations_counter = 0
        nodes = d.get_trajectory().node_id_list
        
        for node in nodes:
            if node[0] == "S":
                stations_counter += 1
        
        resulting_list.append(stations_counter)
        count_percentage[stations_counter] +=1

    count_percentage = [x*100/len(drivers_list) for x in count_percentage]

    import pandas as pd
    import seaborn as sns

    df = pd.DataFrame({"Number of stations visited" :range(3),
    "percentage of drivers" : count_percentage})
    plot = sns.barplot(x="Number of stations visited",y="percentage of drivers",data = df)
    plt.title("Percentage of drivers by number of stations visited")
    if save_path != "":
        plt.savefig(save_path+"/Percentage of drivers by number of stations visited.png",format='png')

    plt.show()
    return resulting_list, count_percentage


