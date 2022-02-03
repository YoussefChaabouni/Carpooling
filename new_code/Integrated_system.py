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
from paper_algorithm_4 import algorithm_4
from paper_algorithm_3 import algorithm_3
from paper_algorithm_2 import algorithm_2
from transit_only import transit_only_algorithm
from check_algorithm_4 import check_algorithm_4


'''
This function will simulate the decision making process of the rider in a current system
he will choose between 3 things : 

- Go on foot
- carpool (m_r_org to m_r_dest) with algorithm 3
- use transit 

this function will return:
t_prime (float): the time taken by the rider in the optimal ride (it's infinity if the rider isn't able to reach r_dst)
solution (string): string expressing the solution the rider has adopted 
(it's "no solution" if the rider can't reach his destination) 

remarks :
- this algorithm will update the riders trajectory according to the adopted solution
'''
def integrated_system(rider : Rider,drivers : List[Driver],graph: Graph):

    t_prime = np.Infinity
    solution = "no solution"
    
    solution_encoding = ["foot","carpooling","transit","integrated"]
    #print("INTEGRATED SYSTEM RESULTS :")
    #print("_______ESTIMATIONS_________________")
    t_foot_prime = walk(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee),graph,rider.walking_speed/60)
    t_carpool = check_algorithm_3(drivers = drivers ,rider =rider ,graph = graph )
    t_transit = transit_only_algorithm(rider,graph)
    t_integrated = check_algorithm_4(drivers = drivers,rider = rider,graph = graph)

    
    # if the rider walks more than 2.5km we set t_foot to infinity
    if graph.get_distance(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee)) > 2.5 :
        t_foot = np.Infinity
    else:
        t_foot = t_foot_prime

    '''
    print("FOOT : ")
    print("    estimated foot time = ",t_foot_prime)
    print("    estimated walking distance = ",graph.get_distance(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee)))
    
    print("________RIDER DECISION PROCESS___________")
    print(" time to CARPOOL = ",t_carpool)
    #print("     estimated time to carpool = ",t_carpool)
    print(" time to go on FOOT = ",t_foot)
    print(" time to TRANSIT = ",t_transit)
    print(" time to integrated = ",t_integrated)
    '''

    solution_times_list = [t_foot,t_carpool,t_transit,t_integrated]


    # see if all the results are infinite and return the solution with best time
    if t_foot == np.Infinity and t_carpool == np.Infinity and t_transit == np.Infinity and t_integrated==np.Infinity:
        #print("the rider has no solution available to him")

        # we update the waiting time to infinity
        rider.update_waiting_time(np.Infinity)
        solution = "no solution"

    else :
        
        idx_min = np.argmin(np.array([t_foot,t_carpool,t_transit,t_integrated])) # minimum solution index
        solution = solution_encoding[idx_min] # adopted solution label
        t_prime = solution_times_list[idx_min] # adopted solution time

        #_____________________________RIDER INFORMATION UPDATES________________________________

        # get origin and destination nodes
        r_org = graph.get_node(rider.pos_depart)
        r_dst = graph.get_node(rider.pos_arrivee)


        if solution == "foot":
           # print("the rider chooses to go on foot")
            arrival_time_destination = rider.born_time + t_foot
            walking_distance = graph.get_distance(graph.get_node(rider.pos_depart),graph.get_node(rider.pos_arrivee))

            # update rider information
            rider.update_walking_distance(walking_distance)
            rider.get_trajectory().update_trajectory(Foot(ID="walk only",Speed=rider.walking_speed/60),arrival_time_destination,arrival_time_destination,r_dst.get_id())

            return t_prime , solution
        if solution == "transit":
           # print("the rider chooses to go with transit")
            # get stations
            s_org = graph.get_closest_MP_or_Station(r_org,"Stations")
            s_dst = graph.get_closest_MP_or_Station(r_dst,"Stations")

            # computing different arrival, departure and waiting times 
            arrival_time_origin_station = rider.born_time + walk(r_org,s_org,graph,rider.walking_speed/60) + 1
            waiting_for_train = next_train_time(s_org,s_dst,arrival_time_origin_station)
            departure_time_origin_station = arrival_time_origin_station + waiting_for_train
            arrival_time_destination_station = board_train(s_org,s_dst,arrival_time_origin_station)
            departure_time_destination_station = arrival_time_destination_station + 1
            arrival_time_destination = departure_time_destination_station + walk(s_dst,r_dst,graph,rider.walking_speed/60)

            #overall walking distance in this option
            walking_distance = graph.get_distance(r_org,s_org) + graph.get_distance(s_dst,r_dst)

            # update rider information
            rider.update_waiting_time(waiting_for_train - arrival_time_origin_station)
            rider.update_walking_distance(walking_distance)
            # walk to station
            rider.get_trajectory().update_trajectory(Foot(ID="walk to first station",Speed=rider.walking_speed/60),arrival_time_origin_station,departure_time_origin_station,s_org.get_id())
            # train ride
            rider.get_trajectory().update_trajectory(Foot(ID="train from "+s_org.get_id()+" to "+s_dst.get_id(),Speed=80/60),arrival_time_destination_station,departure_time_destination_station,s_dst.get_id())
            # walk to destination
            rider.get_trajectory().update_trajectory(Foot(ID="walk to destination "+r_dst.get_id(),Speed=rider.walking_speed/60),arrival_time_destination,arrival_time_destination,r_dst.get_id())
     
        if solution == "carpooling":
           # print("the rider chooses carpooling")
            # the updates are already in algorithm 3 
            #algorithm_3(drivers,rider,graph)
            # update rider trajectory

            m_r_org = graph.get_closest_MP_or_Station(r_org,"MPs").get_id()
            m_r_dest = graph.get_closest_MP_or_Station(r_dst,"MPs").get_id()
            '''
            Le rider va :
            - marcher jusqu'au meeting point m_r_org
            - prendre une voiture jusqu'à m_r_dest
            - marcher jusqu'à r_dest
            '''
            arrival_time_m_r_org = rider.born_time + rider.waiting_time  + walk(r_org,graph.get_node(m_r_org),graph,rider.walking_speed/60) # arrivée à m_r_org
            departure_time_m_r_org = arrival_time_m_r_org #départ de m_r_org
            arrival_time_m_r_dest = departure_time_m_r_org + Drive(graph.get_node(m_r_org),graph.get_node(m_r_dest),graph,40/60) # arrivée à m_r_dest
            departure_time_m_r_dest = arrival_time_m_r_dest # départ de m_r_dest
            arrival_time_r_dest = departure_time_m_r_dest + walk(graph.get_node(m_r_dest),r_dst,graph,rider.walking_speed/60) #arrivée à r_dest
            departure_time_r_dest = arrival_time_r_dest # départ de r_dest

            ## new_mean : Mean_of_transportation,new_arr_time,new_dep_time,new_node_id : int
            rider.get_trajectory().update_trajectory(Foot(ID=m_r_org,Speed=rider.walking_speed),arrival_time_m_r_org,departure_time_m_r_org,m_r_org)
            rider.get_trajectory().update_trajectory(Foot(ID=m_r_org,Speed=rider.walking_speed),arrival_time_m_r_dest,departure_time_m_r_dest,m_r_dest)
            rider.get_trajectory().update_trajectory(Foot(ID = r_dst.get_id(),Speed=rider.walking_speed),arrival_time_r_dest,departure_time_r_dest,r_dst.get_id())

            # update driver's capacity
            '''
            if best_driver != None:
                
                idx_board = best_driver.get_trajectory().node_id_list.index(best_m_d_org)
                idx_out = best_driver.get_trajectory().node_id_list.index(best_m_d_dest)
                for i in range(idx_board,idx_out+1):
                    best_driver.get_current_capacity()[i] +=(-1)
                print("driver ID = ",best_driver.get_id())
                print("current capacity of driver = ",best_driver.get_current_capacity())
            '''
        if solution == "integrated":
            algorithm_4(drivers,rider,graph)
        
    return t_prime , solution
