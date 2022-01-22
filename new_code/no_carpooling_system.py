from typing import List
import numpy as np
from numpy.core.numeric import Infinity
from PersonClasses import Rider, Driver
from graphClasses import Graph
from helperFunctions import walk
from check_algorithm_3 import check_algorithm_3
from meansClasses import Foot
from helperFunctions import board_train, next_train_time
from helperFunctions import Drive
from paper_algorithm_3 import algorithm_3
from paper_algorithm_2 import algorithm_2
from transit_only import transit_only_algorithm


'''
This function will simulate the decision making process of the rider in a no carpooling system
he will choose between 2 things : 

- Go on foot
- use transit 

this function will return:
t_prime (float): the time taken by the rider in the optimal ride (it's infinity if the rider isn't able to reach r_dst)
solution (string): string expressing the solution the rider has adopted 
(it's "no solution" if the rider can't reach his destination) 

remarks :
- this algorithm will update the riders trajectory according to the adopted solution
'''
def no_carpooling_system(rider : Rider,graph: Graph):

    t_prime = np.Infinity
    solution = "no solution"
    
    solution_encoding = ["foot","transit"]
    #print("NO CARPOOLING SYSTEM RESULTS :")
    #print("_______ESTIMATIONS_________________")
    t_foot_prime = walk(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee),graph,4.5/60)
    t_transit = transit_only_algorithm(rider,graph)

    
    # if the rider walks more than 2.5km we set t_foot to infinity
    if graph.get_distance(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee)) > 2.5 :
        t_foot = np.Infinity
    else:
        t_foot = t_foot_prime

    
    #print("FOOT : ")
    #print("    estimated foot time = ",t_foot_prime)
    #print("    estimated walking distance = ",graph.get_distance(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee)))
    
    #print("________RIDER DECISION PROCESS___________")
    
    #print("     estimated time to carpool = ",t_carpool)
    #print(" time to go on FOOT = ",t_foot)
    #print(" time to TRANSIT = ",t_transit)


    solution_times_list = [t_foot,t_transit]


    # see if all the results are infinite and return the solution with best time
    if t_foot == np.Infinity  and t_transit == np.Infinity:
        #print("the rider has no solution available to him")

        # we update the waiting time to infinity
        rider.update_waiting_time(np.Infinity)
        solution = "no solution"

    else :
        
        idx_min = np.argmin(np.array([t_foot,t_transit])) # minimum solution index
        solution = solution_encoding[idx_min] # adopted solution label
        t_prime = solution_times_list[idx_min] # adopted solution time

        #_____________________________RIDER INFORMATION UPDATES________________________________

        # get origin and destination nodes
        r_org = graph.get_node(rider.pos_depart)
        r_dst = graph.get_node(rider.pos_arrivee)


        if solution == "foot":
            #print("the rider chooses to go on foot")
            arrival_time_destination = rider.born_time + t_foot
            walking_distance = graph.get_distance(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee))

            # update rider information
            rider.update_walking_distance(walking_distance)
            rider.get_trajectory().update_trajectory(Foot(ID="walk only",Speed=4.5/60),arrival_time_destination,arrival_time_destination,r_dst.get_id())

            return t_prime , solution
        if solution == "transit":
            #print("the rider chooses to go with transit")
            # get stations
            s_org = graph.get_closest_MP_or_Station(r_org,"Stations")
            s_dst = graph.get_closest_MP_or_Station(r_dst,"Stations")

            # computing different arrival, departure and waiting times 
            arrival_time_origin_station = rider.born_time + walk(r_org,s_org,graph,4.5/60) + 1
            waiting_for_train = next_train_time(s_org,s_dst,arrival_time_origin_station)
            departure_time_origin_station = arrival_time_origin_station + waiting_for_train
            arrival_time_destination_station = board_train(s_org,s_dst,arrival_time_origin_station)
            departure_time_destination_station = arrival_time_destination_station + 1
            arrival_time_destination = departure_time_destination_station + walk(s_dst,r_dst,graph,4.5/60)

            #overall walking distance in this option
            walking_distance = graph.get_distance(r_org,s_org) + graph.get_distance(s_dst,r_dst)

            # update rider information
            rider.update_waiting_time(waiting_for_train - arrival_time_origin_station)
            rider.update_walking_distance(walking_distance)
            # walk to station
            rider.get_trajectory().update_trajectory(Foot(ID="walk to first station",Speed=4.5/60),arrival_time_origin_station,departure_time_origin_station,s_org.get_id())
            # train ride
            rider.get_trajectory().update_trajectory(Foot(ID="train from "+s_org.get_id()+" to "+s_dst.get_id(),Speed=80/60),arrival_time_destination_station,departure_time_destination_station,s_dst.get_id())
            # walk to destination
            rider.get_trajectory().update_trajectory(Foot(ID="walk to destination "+r_dst.get_id(),Speed=4.5/60),arrival_time_destination,arrival_time_destination,r_dst.get_id())
     

    return t_prime , solution
