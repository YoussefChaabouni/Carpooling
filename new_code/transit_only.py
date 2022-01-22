import numpy as np
from PersonClasses import Rider
from graphClasses import Graph
from helperFunctions import walk, board_train

'''
This algorithm measures the time it takes the rider to reach his destination with transit only
outputs :
t_prime (float) : the time it takes the rider using transit (infinity if he can't)

remarks : 
- we penalize this algorithm if s_org and s_dst are the same station
the rider would logically walk straight to the destination
- we update rider trajectory in current_system function this algorithm just checks the time it takes
the trajectory of the rider is at this point hypothetical and doesn't need to be filled
'''

def transit_only_algorithm(rider : Rider, graph : Graph):
    t_prime = np.Infinity

    # initialize the needed nodes
    r_org = graph.get_node(rider.pos_depart)
    r_dst = graph.get_node(rider.pos_arrivee)
    s_org = graph.get_closest_MP_or_Station(r_org,"Stations")
    s_dst = graph.get_closest_MP_or_Station(r_dst,"Stations")
    #print("TRANSIT :")
    #print("    the transit options wants the rider to go from ",s_org.get_id()," to ",s_dst.get_id())
    if s_org.get_id() == s_dst.get_id():
        #this case the rider shouldn't consider the train option
        #the algorithm does nothing to t_prime
        return t_prime

    else :
        # walking to first station 
        t_prime = walk(r_org,s_org,graph,5/60) + 1
        arrival_time_org_station = rider.born_time + t_prime # arrival time to station

        # boarding the train
        t_prime += board_train(s_org,s_dst,arrival_time_org_station) - arrival_time_org_station #duration of train trip

        # walking to destination
        t_prime += walk(s_dst,r_dst,graph,5/60) + 1

        # compute the overall walking distance to check if the rider can consider the trip
        
        #print("     the estimated time using transit is = ",t_prime)
        walking_distance = graph.get_distance(r_org,s_org) + graph.get_distance(s_dst,r_dst)
        if walking_distance > 2.5 :
            #print("    the estimated walking distance in transit option = ",walking_distance)
            t_prime = np.Infinity
        
        return t_prime
